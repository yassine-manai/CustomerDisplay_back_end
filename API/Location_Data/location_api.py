import json
from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from Manager.WebSocket import manager
from Models.items import Locationdata
from config.log_config import logger

app = FastAPI()

LocationData = APIRouter()  # This is for location data

# File path for the local JSON data
LOCAL_DATA_FILE = "local_data.json"

# Function to load data from the local JSON file
def load_local_data():
    try:
        with open(LOCAL_DATA_FILE, 'r') as file:
            data = json.load(file)
            logger.info("Local data loaded successfully")
            return data
    except FileNotFoundError:
        logger.error("Local data file not found")
        return {}
    except json.JSONDecodeError:
        logger.error("Failed to decode JSON data")
        raise HTTPException(status_code=500, detail="Failed to decode JSON data")

# Function to save data to the local JSON file
def save_local_data(data):
    try:
        with open(LOCAL_DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)
            logger.info("Local data saved successfully")
    except Exception as e:
        logger.error(f"Failed to save data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save data: {e}")

# Location WebSocket
@LocationData.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"Received message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Location Data EndPoint
@LocationData.post("/locationData")
async def Location_Data(item: Locationdata):
    """
    ## **Location Data**:

    * **message**  the message 100
    * **Icon**  the image icon base64 format.
    * **Name_Point**  the Location Name passed as String.
    * **Exit_Point**  the Exit Name passed as String.
    * **TimeZone**  the Time Zone passed as String (Default is "Asia/Kuwait").

                - TimeZones list : \n
                          Middle East TimeZone Identifiers :                              |      Africa TimeZone Identifiers : 
                                                                                          |
                                                        "Asia/Aden"                       |                        "Africa/Cairo"
                                                        "Asia/Amman"                      |                        "Africa/Casablanca"
                                                        "Asia/Baghdad"                    |                        "Africa/Dakar"
                                                        "Asia/Bahrain"                    |                        "Africa/El_Aaiun"
                                                        "Asia/Beirut"                     |                        "Africa/El_Aaiun"
                                                        "Asia/Damascus"                   |                        "Africa/Harare"
                                                        "Asia/Doha"                       |                        "Africa/Tripoli"
                                                        "Asia/Gaza"                       |                        "Africa/Tunis"
                                                        "Asia/Hebron"                     |                        "Africa/Lagos"
                                                        "Asia/Kuwait"                     |                        "Africa/Khartoum"
                                                        "Asia/Nicosia"                    |                        "Africa/Lome"
                                                        "Asia/Qatar"                      |                        "Africa/Nairobi"
                                                        "Asia/Riyadh"                     |                        "Africa/Maputo"
    """
    try:
        # Load existing data from the local JSON file
        local_data = load_local_data()

        # Update local data with the new values
        local_data["name_point"] = item.name_point
        local_data["exit_point"] = item.exit_point
        local_data["timezone"] = item.timezone

        # Save the updated data back to the local JSON file
        save_local_data(local_data)

        # Processed data to be broadcasted
        processed_data = {
            "message": 100,
            "icon": item.icon,
            "name_point": item.name_point,
            "exit_point": item.exit_point,
            "timezone": item.timezone,
        }
        await manager.broadcast(processed_data)
        return processed_data
    except Exception as e:
        logger.error(f"Failed to process request: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process request: {e}")

app.include_router(LocationData)
