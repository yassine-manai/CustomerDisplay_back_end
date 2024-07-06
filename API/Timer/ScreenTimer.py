from asyncio import sleep
import base64
import os
from dotenv import load_dotenv
import requests
from fastapi import FastAPI, HTTPException, APIRouter
from config.log_config import logger
from config.config import OPERATOR_ID, SAVE_PATH, SERVER_IP, SERVER_PORT, ZR_ID
from config.run_thread import run_in_thread

# Load environment variables
load_dotenv()

app = FastAPI()
TimersData = APIRouter() 

def fetch_timers():
    url = f"http://{SERVER_IP}:{SERVER_PORT}/internal/api/getAds?operator_id={OPERATOR_ID}&zr_id={ZR_ID}"
    logger.info(url)

    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()

            if data.get("success"):
                banner_change_time = data["data"].get("bannerChangeTime", "6")
                main_screen_change_time = data["data"].get("mainScreenChangeTime", "6")
                
                logger.info(f"Banner Change Time: {banner_change_time}")
                logger.info(f"Main Screen Change Time: {main_screen_change_time}")
                
                ads_data = {
                    'banner_time': banner_change_time,
                    'main_time': main_screen_change_time,
                }
                
                return ads_data

                logger.info("Data successfully")
            else:
                logger.error(f"API error: {data.get('error')}")
        else:
            logger.error(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Exception occurred: {e}")



@TimersData.get("/main-timer")
async def get_timers_data():
    data = fetch_timers()
    if data:
        logger.success(f"Timers Fetched: {data}")
        return data
    raise HTTPException(status_code=404, detail="Data not found")
