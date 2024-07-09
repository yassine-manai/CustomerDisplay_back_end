import requests
import json
import os
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from config.log_config import logger
from Models.items import Locationdata
from fastapi.middleware.cors import CORSMiddleware
from config.config import POS_IP,POS_PORT,POS_API
from config.run_thread import run_in_thread
from Manager.local_config import load_local_config, save_local_config


app = FastAPI()
UpdateLocData = APIRouter() 


# File to store the local data
LOCAL_DATA_FILE = "local_data.json"

@run_in_thread
def fetch_and_save_data():
    logger.info("Starting data fetch and save process")

    try:
        response = requests.get(f"http://{POS_IP}:{POS_PORT}/{POS_API}")

        response.raise_for_status()  
        data = response.json()
        
        logger.debug(f"Received data from POS API: {data}")

        carpark_name = data.get('carParkName')
        posName = data.get('posName')
        operator_id = data.get('operatorId')
        zr_id = data.get('zrId')
        pos_id = data.get('posId')


        local_data = {
            'name_point': carpark_name,
            'exit_point': posName,
            'operator_id': operator_id,
            'zr_id': zr_id,
            'pos_id': pos_id,
            'timezone': "Asia/Kuwait",
        }
        
        # Save data locally
        save_local_config(local_data)
        
        logger.success(f"Data saved locally: {local_data}")
        
    except requests.RequestException as e:
        logger.error(f"An error occurred while fetching data: {e}")

@UpdateLocData.get("/infos/get_location_data")
def get_location_data():
    data = load_local_config()
    if data:
        logger.success(f"Data Fetched: {data}")
        return data
    raise HTTPException(status_code=404, detail="Location data not found")


