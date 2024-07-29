import os
import base64
import requests
from Models.items import AdsImagesData
from config.log_config import logger
from config.config import SERVER_IP, SERVER_PORT
from globalvars.globals import local_data



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



def cleanlistimages(img: list)->str:
    retlist=[]
    for image in img:
        retlist.append(image.replace('data:','').strip())
    return retlist


def fetch_images() -> AdsImagesData:
    global local_data
    
    OPERATOR_ID = local_data.get("operator_id")
    ZR_ID = local_data.get("zr_id")
    POS_ID = local_data.get("pos_id")
    
    logger.debug("Call Parking Control started :--------------------------------------:",local_data)
    
    url = f"http://{SERVER_IP}:{SERVER_PORT}/internal/api/getAds?operator_id={OPERATOR_ID}&zr_id={ZR_ID}&pos_id={POS_ID}"
    logger.info(url)
    
    logger.debug(" Call Ended :--------------------------------------: ",url)

    try:
        response = requests.get(url)
        response.raise_for_status() 
        
        response_json = response.json()
        logger.debug(f"Banner Length:{len(response_json['data']['bannerImages'])} / mainscreen len {len(response_json['data']['mainScreenImages'])}" )
        
        if response_json.get("success"):
            banner= cleanlistimages(response_json['data']['bannerImages'])
            mainScreenImages= cleanlistimages(response_json['data']['mainScreenImages'])
            
            data = AdsImagesData(
                bannerImages=banner,
                mainScreenImages=mainScreenImages,
                bannerChangeTime=int(response_json['data']['bannerChangeTime']),
                mainScreenChangeTime=int(response_json['data']['mainScreenChangeTime']),
            )
            return data
        else:
            logger.error(f"API error: {response_json.get('error')}")
    except Exception as e:
        logger.error(f"Exception occurred: {e}")


