import json
import os
from asyncio import sleep
import base64
import requests
from config.log_config import logger
from config.config import SAVE_PATH, SERVER_IP, SERVER_PORT
from config.run_thread import run_in_thread

# Load the local.json file
def load_local_config():
    with open('local_data.json', 'r') as f:
        config = json.load(f)
    return config

local_config = load_local_config()
OPERATOR_ID = local_config.get("operator_id")
ZR_ID = local_config.get("zr_id")

def get_image_extension(image_data):
    if image_data.startswith("data:image/jpeg"):
        return "jpeg"
    elif image_data.startswith("data:image/png"):
        return "png"
    else:
        return "jpg"

def save_images(image_data, prefix):
    images_path = os.path.join(os.path.dirname(__file__), 'images')
    if not os.path.exists(images_path):
        os.makedirs(images_path)
    
    existing_files = set(os.listdir(images_path))
    new_files = set()
    counter = 1
    
    for image in image_data:
        extension = get_image_extension(image)
        image_path = os.path.join(images_path, f"{prefix}_{counter}.{extension}")
        new_files.add(f"{prefix}_{counter}.{extension}")

        with open(image_path, "wb") as img_file:
            img_file.write(base64.b64decode(image.split(",")[1]))  
                 
        counter += 1
    
    files_to_remove = existing_files - new_files
    for file in files_to_remove:
        os.remove(os.path.join(images_path, file))

def process_images(api_response):
    if api_response.get("success"):
        data = api_response.get("data", {})
        
        # Process bannerImages
        banner_images = data.get("bannerImages", [])
        if (banner_images):
            logger.info("Processing banner images")
            save_images(banner_images, "banner")

        # Process mainScreenImages
        main_screen_images = data.get("mainScreenImages", [])
        if (main_screen_images):
            logger.info("Processing main screen images")
            save_images(main_screen_images, "main_screen")
    else:
        logger.error("API call was not successful")

def fetch_and_save_images():
    url = f"http://{SERVER_IP}:{SERVER_PORT}/internal/api/getAds?operator_id={OPERATOR_ID}&zr_id={ZR_ID}"
    
    print(OPERATOR_ID)

    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()

            if data.get("success"):
                process_images(data)
                logger.info("Images processed successfully")
            else:
                logger.error(f"API error: {data.get('error')}")
        else:
            logger.error(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
