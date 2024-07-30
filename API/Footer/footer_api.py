from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from Manager.WebSocket import manager
from Models.items import footerData
from config.log_config import logger

app = FastAPI()

FooterData = APIRouter()

# Footer Data WebSocket
@FooterData.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"Received message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Footer Data Endpoint
@FooterData.post("/footer_data")
async def footer_data(item: footerData):
    """
    ## **Location Data**: 
    * **message**: the message 110
    * **timerIntervale**: the image passed as base64 format.
    """
    try:
        processed_data = {
            "message": 110,
            "timerIntervale": item.timerIntervale,
        }
        await manager.broadcast(processed_data)
        logger.info(f"Processed data: {processed_data}")
        return processed_data
    except Exception as e:
        logger.error(f"Failed to process request: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process request: {e}")

