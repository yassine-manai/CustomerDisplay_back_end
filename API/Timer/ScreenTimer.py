import base64
import os
import time
from dotenv import load_dotenv
import requests
from fastapi import FastAPI, HTTPException, APIRouter
from config.log_config import logger
from config.config import SERVER_IP, SERVER_PORT, IMAGES_PATH, CRON
from API.imageLoader.images_load import fetch_images as original_fetch_images, get_image_extension
from globalvars.globals import local_data

app = FastAPI()

GetTimersData = APIRouter()
UpdateTimersData = APIRouter()
UpdateAdsData = APIRouter()


def fetch_images():
    try:
        images = original_fetch_images()
        if not images:
            logger.error("fetch_images: No images returned from the API")
            return None
        
        if not hasattr(images, 'bannerImages') or not hasattr(images, 'mainScreenImages'):
            logger.error("fetch_images: Returned object does not have the expected attributes")
            return None
        
        return images

    except Exception as e:
        logger.error(f"Exception in fetch_images: {e}")
        return None

def fetch_timers():
    global local_data
    
    OPERATOR_ID = local_data.get("operator_id")
    ZR_ID = local_data.get("zr_id")
    POS_ID = local_data.get("pos_id")
        
    url = f"http://{SERVER_IP}:{SERVER_PORT}/internal/api/getAds?operator_id={OPERATOR_ID}&zr_id={ZR_ID}&pos_id={POS_ID}"
    logger.debug(url)
    
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                
                banner_change_time = int(data["data"].get("bannerChangeTime", "10"))
                main_screen_change_time = int(data["data"].get("mainScreenChangeTime", "10"))


                logger.info(f"Banner Change Time: {banner_change_time}")
                logger.info(f"Main Screen Change Time: {main_screen_change_time}")
                logger.info(f"CRON Change Time: {CRON}")

                ads_timers = {
                    'banner_time': banner_change_time,
                    'main_time': main_screen_change_time,
                    'cron': CRON
                }
                
                
                local_data['banner_time'] = banner_change_time
                local_data['main_time'] = main_screen_change_time
                local_data['cron'] = CRON


                logger.info("Data successfully fetched and saved to local config")
                return ads_timers
            else:
                logger.error(f"API error: {data.get('error')}")
        else:
            logger.error(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
    return None


def save_images(image_data: list, prefix: str):
    images_path = os.path.join(os.path.dirname(__file__), IMAGES_PATH)
    if not os.path.exists(images_path):
        os.makedirs(images_path)
    
    if len(image_data) > 0:
        files = os.listdir(images_path)
        for file in files:
            if file.startswith(prefix):
                file_path = os.path.join(images_path, file)
                try:
                    os.remove(file_path)
                    #print(f"Removed file: {file_path}")
                except Exception as e:
                    print(f"Error removing file: {file_path} - {e}")

    existing_files = set(os.listdir(images_path))
    new_files = set()
    counter = 1
    logger.debug(f"Save process {prefix} {len(image_data)} element")
    for image in image_data:
        extension = get_image_extension(image)
        image_data_parts = image.split(",")
        image_base64 = image_data_parts[1] if len(image_data_parts) > 1 else ""
        image_path = os.path.join(images_path, f"{prefix}_{counter}.{extension}")
        new_files.add(f"{prefix}_{counter}.{extension}")
        logger.debug(f"Process image {image_path}")
        if extension == "svg":
            svg_data = image_base64
            svg_content = base64.b64decode(svg_data).decode("utf-8")
            with open(image_path, "w") as img_file:
                img_file.write(svg_content)
        else:
            with open(image_path, "wb") as img_file:
                ret = img_file.write(base64.b64decode(image_base64))
                logger.debug(f"Response save image {ret}")
        time.sleep(0.5)
        counter += 1

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
    global local_data
    
    OPERATOR_ID = local_data.get("operator_id")
    ZR_ID = local_data.get("zr_id")
    POS_ID = local_data.get("pos_id")
        
    url = f"http://{SERVER_IP}:{SERVER_PORT}/internal/api/getAds?operator_id={OPERATOR_ID}&zr_id={ZR_ID}&pos_id={POS_ID}"
    logger.debug(url)
    
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






def update_images_from_control():
    fetch_timers()
    allimages = fetch_images()
    if allimages is None:
        logger.error("Failed to fetch images. Skipping call.")
        return

    if hasattr(allimages, 'bannerImages'):
        save_images(allimages.bannerImages, "banner")
    else:
        logger.error("allimages does not have bannerImages attribute.")

    if hasattr(allimages, 'mainScreenImages'):
        save_images(allimages.mainScreenImages, "main_screen")
    else:
        logger.error("allimages does not have mainScreenImages attribute.")









@GetTimersData.get("/ads_timer")
async def get_timers_data():
    global local_data
    
    timers_data = {
        "banner_time": local_data.get("banner_time",10),
        "main_time": local_data.get("main_time",10),
        "cron": local_data.get("cron",1)
    }
    logger.success(f"Timers Fetched from local config: {timers_data}")
    return timers_data


@UpdateAdsData.post("/update_ads")
async def update_ads_data():
    allimages = fetch_images()
    fetch_timers()
    
    if allimages is None:
        logger.error("Failed to fetch images. Skipping update.")
        raise HTTPException(status_code=500, detail="Failed to fetch images from API")

    if hasattr(allimages, 'bannerImages'):
        save_images(allimages.bannerImages, "banner")
    else:
        logger.error("allimages does not have bannerImages attribute.")
        raise HTTPException(status_code=500, detail="API response missing bannerImages attribute")

    if hasattr(allimages, 'mainScreenImages'):
        save_images(allimages.mainScreenImages, "main_screen")
    else:
        logger.error("allimages does not have mainScreenImages attribute.")
        raise HTTPException(status_code=500, detail="API response missing mainScreenImages attribute")

    return {"detail": "Ads data fetched from API and updated"}
























""" @UpdateTimersData.post("/update_timers")
async def update_timers_data(
    main_timer: int = Query(None, description="timer in seconds."),
    banner_timer: int = Query(None, description="timer in seconds."),
    cron_timer: int = Query(None, description="timer in hours."),
):
    
    Update Timers:

    Parameters:
    - main_timer (int, optional): Main screen change timer in seconds.
    - banner_timer (int, optional): Banner change timer in seconds.
    - cron_timer (int, optional): Cron job interval in hours.
    
    
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
        
        save_local_config(local_config, LOCAL_DATA_FILE)
        return {"detail": "Timers data updated with provided parameters"}
 """