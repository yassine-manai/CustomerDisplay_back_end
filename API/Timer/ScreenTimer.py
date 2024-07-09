import base64
import os
from dotenv import load_dotenv
import requests
from fastapi import FastAPI, HTTPException, APIRouter, Query
from config.log_config import logger
from config.config import SAVE_PATH, SERVER_IP, SERVER_PORT, IMAGES_PATH, CRON
from config.run_thread import run_in_thread
from Manager.local_config import load_local_config, save_local_config

app = FastAPI()

GetTimersData = APIRouter()
UpdateTimersData = APIRouter()
UpdateAdsData = APIRouter()

local_config = load_local_config()

OPERATOR_ID = local_config.get("operator_id")
ZR_ID = local_config.get("zr_id")
POS_ID = local_config.get("pos_id")

url = f"http://{SERVER_IP}:{SERVER_PORT}/internal/api/getAds?operator_id={OPERATOR_ID}&zr_id={ZR_ID}&pos_id={POS_ID}"

def fetch_timers():
    logger.info(url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                banner_change_time = int(data["data"].get("bannerChangeTime", "10"))
                main_screen_change_time = int(data["data"].get("mainScreenChangeTime", "10"))
                cron = int(CRON, 10)

                logger.info(f"Banner Change Time: {banner_change_time}")
                logger.info(f"Main Screen Change Time: {main_screen_change_time}")
                logger.info(f"CRON Change Time: {cron}")

                ads_timers = {
                    'banner_time': banner_change_time,
                    'main_time': main_screen_change_time,
                    'cron': cron
                }

                # Save the fetched timers to local_config and persist the changes
                local_config.update(ads_timers)
                save_local_config(local_config)

                logger.info("Data successfully fetched and saved to local config")
                return ads_timers
            else:
                logger.error(f"API error: {data.get('error')}")
        else:
            logger.error(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
    return None

def get_image_extension(image_data):
    if image_data.startswith("data:image/jpeg"):
        return "jpeg"
    elif image_data.startswith("data:image/png"):
        return "png"
    elif image_data.startswith("data:image/svg+xml"):
        return "svg"
    else:
        return "jpg"

def save_images(image_data, prefix):
    images_path = os.path.join(os.path.dirname(__file__), IMAGES_PATH)
    if not os.path.exists(images_path):
        os.makedirs(images_path)
    
    existing_files = set(os.listdir(images_path))
    new_files = set()
    counter = 1
    
    for image in image_data:
        extension = get_image_extension(image)
        image_data_parts = image.split(",")
        image_base64 = image_data_parts[1] if len(image_data_parts) > 1 else ""
        image_path = os.path.join(images_path, f"{prefix}_{counter}.{extension}")
        new_files.add(f"{prefix}_{counter}.{extension}")

        if extension == "svg":
            svg_data = image_base64
            svg_content = base64.b64decode(svg_data).decode("utf-8")
            with open(image_path, "w") as img_file:
                img_file.write(svg_content)
        else:
            with open(image_path, "wb") as img_file:
                img_file.write(base64.b64decode(image_base64))
                 
        counter += 1
    
    files_to_remove = existing_files - new_files
    for file in files_to_remove:
        os.remove(os.path.join(images_path, file))

def process_images(api_response):
    if api_response.get("success"):
        data = api_response.get("data", {})
        
        # Process bannerImages
        banner_images = data.get("bannerImages", [])
        if banner_images:
            logger.info("Processing banner images")
            save_images(banner_images, "banner")

        # Process mainScreenImages
        main_screen_images = data.get("mainScreenImages", [])
        if main_screen_images:
            logger.info("Processing main screen images")
            save_images(main_screen_images, "main_screen")
    else:
        logger.error("API call was not successful")

def fetch_and_save_images():
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

def update_local_config_with_timers():
    timers_data = fetch_timers()
    if timers_data:
        local_config.update(timers_data)
        save_local_config(local_config)
        logger.info("Local config updated")
    else:
        logger.error("Failed to update local config")

def update_local_config():
    fetch_and_save_images()
    update_local_config_with_timers()

@GetTimersData.get("/ads_timer")
async def get_timers_data():
    local_config = load_local_config()
    if "banner_time" in local_config and "main_time" in local_config:
        timers_data = {
            "banner_time": local_config["banner_time"],
            "main_time": local_config["main_time"],
            "cron": local_config["cron"]
        }
        logger.success(f"Timers Fetched from local config: {timers_data}")
        return timers_data
    raise HTTPException(status_code=404, detail="Timers data not found")

@UpdateTimersData.post("/update_timers")
async def update_timers_data(
    main_timer: int = Query(None, description="timer in seconds."),
    banner_timer: int = Query(None, description="timer in seconds."),
    cron_timer: int = Query(None, description="timer in hours."),
):
    """
    Update Timers:

    Parameters:
    - main_timer (int, optional): Main screen change timer in seconds.
    - banner_timer (int, optional): Banner change timer in seconds.
    - cron_timer (int, optional): Cron job interval in hours.
    """
    
    if main_timer is None and banner_timer is None and cron_timer is None:
        update_local_config_with_timers()
        return {"detail": "Timers data fetched from API and updated"}
    else:
        if main_timer is not None:
            local_config["main_time"] = main_timer
            logger.info(f"Main Screen Change Time updated to: {main_timer}")
        
        if banner_timer is not None:
            local_config["banner_time"] = banner_timer
            logger.info(f"Banner Change Time updated to: {banner_timer}")
        
        if cron_timer is not None:
            local_config["cron"] = cron_timer
            logger.info(f"Cron Change Time updated to: {cron_timer}")
        
        save_local_config(local_config)
        return {"detail": "Timers data updated with provided parameters"}

@UpdateAdsData.post("/update_ads")
async def update_ads_data():
    fetch_and_save_images()
    return {"detail": "Ads data fetched from API and updated"}