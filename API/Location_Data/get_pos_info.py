import requests
from fastapi import FastAPI, APIRouter, HTTPException
from config.log_config import logger
from config.config import POS_IP,POS_PORT,POS_API,TZ

from globalvars.globals import local_data

app = FastAPI()
UpdateLocData = APIRouter() 


def get_data_from_pos() -> bool:
    global local_data
    
    """Fetches data from POS API and saves it locally."""
    
    logger.info("*** Starting data fetch and save process ***")
    try:
        response = requests.get(f"http://{POS_IP}:{POS_PORT}/{POS_API}")
        response.raise_for_status()
        
        data = response.json()
        
        data_log={
            "carParkName":data.get('carParkName'),
            "posName":data.get('posName'),
            "operatorId": data.get('operatorId'),
            "zrId":data.get('zrId'),
            "posId":data.get('posId')
        }
        
        logger.debug(f"Response From POS {data_log}")
        
        local_data['name_point'] = data.get('carParkName',"Default")
        local_data['exit_point'] = data.get('posName',"Defaultposname")
        local_data['operator_id'] = data.get('operatorId',99000)
        local_data['zr_id'] = data.get('zrId',7000)
        local_data['pos_id'] = data.get('posId',701)
        local_data['timezone'] = TZ if TZ else 'Etc/UTC'
        
        logger.debug(f"New data object API: {local_data}")
        return True
    
    except requests.RequestException as e:
        logger.error(f"An error occurred while fetching data: {e}")
        return False

@UpdateLocData.get("/infos/get_location_data")
def get_location_data(): 
    if not local_data: 
        raise HTTPException(status_code=404, detail="No location data found")
    return local_data
 