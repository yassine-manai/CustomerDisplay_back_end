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

app = FastAPI()
UpdateLocData = APIRouter() 


# File to store the local data
LOCAL_DATA_FILE = "local_data.json"


def save_local_data(data):
    with open(LOCAL_DATA_FILE, 'w') as f:
        json.dump(data, f)

def load_local_data():
    if os.path.exists(LOCAL_DATA_FILE):
        with open(LOCAL_DATA_FILE, 'r') as f:
            return json.load(f)
    return None

def fetch_and_save_data():
    logger.info("Starting data fetch and save process")

    try:
        response = requests.get(f"http://{POS_IP}:{POS_PORT}/{POS_API}")

        response.raise_for_status()  
        data = response.json()
        
        logger.debug(f"Received data from POS API: {data}")

        # Extract required information
        carpark_name = data.get('carParkName')
        posName = data.get('posName')
        operator_id = data.get('operatorId')
        zr_id = data.get('zrId')


        # Prepare data for local storage
        local_data = {
            'name_point': carpark_name,
            'exit_point': posName,
            'operator_id': operator_id,
            'zr_id': zr_id,
            'timezone': "Asia/Kuwait"
        }
        
        # Save data locally
        save_local_data(local_data)
        
        logger.success(f"Data saved locally: {local_data}")
        
    except requests.RequestException as e:
        logger.error(f"An error occurred while fetching data: {e}")

@UpdateLocData.get("/locationData")
async def get_location_data():
    #fetch_and_save_data()
    data = load_local_data()
    if data:
        logger.success(f"Data Fetched: {data}")
        return data
    raise HTTPException(status_code=404, detail="Location data not found")


