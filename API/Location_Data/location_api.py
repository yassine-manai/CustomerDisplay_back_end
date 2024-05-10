from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from Manager.WebSocket import manager
from Models.items import Locationdata

app = FastAPI()

LocationData = APIRouter() #This is for location data

#Location WebSocket
@LocationData.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            print(f"Received message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)


#Location Data EndPoint
@LocationData.post("/locationData")
async def Location_Data(item: Locationdata):

    """

        ## **Location Data**: 

        * **messaage**  the message 100
        * **Icon**  the image icon base64 format.
        * **Name**  the Location Name passed as String.
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
        processed_data = {
            "message": 100,
            "icon": item.icon,
            "name": item.name,
            "exit_point": item.exit_point,
            "timezone": item.timezone,
        }
        await manager.broadcast(processed_data)
        return processed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process request: {e}")
