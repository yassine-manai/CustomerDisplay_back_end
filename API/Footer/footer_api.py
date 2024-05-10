from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from Manager.WebSocket import manager
from Models.items import footerData

app = FastAPI()

FooterData = APIRouter() #This is for footer data

#Location WebSocket
@FooterData.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            print(f"Received message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)


#Location Data EndPoint
@FooterData.post("/footerData")
async def Footer_Data(item: footerData):

    """

        ## **Location Data**: 

        * **messaage**  the message 110
        * **timerIntervale**  the image passed as base64 format.

    """
    try:
        processed_data = {
            "message": 110,
            "timerIntervale": item.timerIntervale,
        }
        await manager.broadcast(processed_data)
        return processed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process request: {e}")
