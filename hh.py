pythonCopyimport requests
from config.log_config import logger
from pydantic import BaseModel
from Models.items import Locationdata

def Location_Data(location_config: Locationdata):
    """
    Function to process location data.
    """
    logger.info(f"Processing location data: {location_config}")
    # Add your logic here to process the location data
    
    # Simulating a successful operation
    return {"status": "success", "message": f"Data processed for {location_config.name_point} at exit {location_config.exit_point}"}

def handle_location_data(payload):
    """
    Function to handle location data locally by calling Location_Data function.
    """
    logger.info(f"Handling location data locally: {payload}")
    
    try:
        location_config = Locationdata(
            name_point=payload['name_point'],
            exit_point=payload['exit_point']
        )
    except ValueError as e:
        logger.error(f"Invalid payload: {e}")
        return False
    
    result = Location_Data(location_config)
    
    if result.get('status') == 'success':
        logger.success(f"Data processed successfully: {result['message']}")
        return True
    else:
        logger.error(f"Failed to process data: {result.get('message', 'Unknown error')}")
        return False

def fetch_and_send_data():
    logger.info("Starting data fetch and send process")

    # Fetch data from the first API
    try:
        response = requests.get('http://192.168.1.7:8000/local/pos_config')
        response.raise_for_status()  
        data = response.json()
        
        logger.debug(f"Received data from first API: {data}")

        # Extract required information
        carpark_name = data.get('carParkName')
        pos_id = data.get('posId')
        
        # Prepare data for local handling
        payload = {
            'name_point': carpark_name,
            'exit_point': pos_id
        }
        
        logger.info(f"Prepared payload: {payload}")

        # Handle data locally
        result = handle_location_data(payload)
        
        if result:
            logger.success(f"Data processed successfully: {payload}")
        else:
            logger.error(f"Failed to process data: {payload}")
        
    except requests.RequestException as e:
        logger.error(f"An error occurred while fetching data: {e}")

