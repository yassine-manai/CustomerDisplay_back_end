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

        * **Icon**  the image icon base64 format.
        * **Name**  the Location Name passed as String.
        * **Exit**  the Exit Name passed as String.

    """
    try:
        processed_data = {
            "icon": item.icon,
            "name": item.name,
            "exit": item.exit,
        }
        await manager.broadcast(processed_data)
        return processed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process request: {e}")
