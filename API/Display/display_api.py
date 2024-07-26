from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from Manager.WebSocket import manager
from Models.items import *
from config.log_config import logger
from config.ws_helper import common_websocket_endpoint

app = FastAPI()

Idle = APIRouter()  # Idle Model ADS Main Screen (1)
Stppd = APIRouter()  # Short term parker-Price display (2)
Estpgm = APIRouter()  # Exit short term parker - Goodbye message (3)
Paygm = APIRouter()  # Pay as you go-GOODBYE Message (4)
Psgm = APIRouter()  # Prebooking + Subscriber - GOODBYE Message (5)

# Common WebSocket endpoint handler
async def common_websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"Received message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        

async def broadcast_and_log(processed_data, model_name):
    try:
        log_data = processed_data.copy()
        if "carImage" in log_data:
            log_data.pop("carImage")

        await manager.broadcast(processed_data)
        logger.info(f"{model_name} - Processed data: {log_data}")
        return processed_data
    except Exception as e:
        logger.error(f"{model_name} - Failed to process request: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process request: {e}")
    

# WebSocket endpoints
@Idle.websocket("/ws")
async def websocket_endpoint_idle(websocket: WebSocket):
    await common_websocket_endpoint(websocket)

@Stppd.websocket("/ws")
async def websocket_endpoint_stppd(websocket: WebSocket):
    await common_websocket_endpoint(websocket)

@Estpgm.websocket("/ws")
async def websocket_endpoint_estpgm(websocket: WebSocket):
    await common_websocket_endpoint(websocket)

@Paygm.websocket("/ws")
async def websocket_endpoint_paygm(websocket: WebSocket):
    await common_websocket_endpoint(websocket)

@Psgm.websocket("/ws")
async def websocket_endpoint_psgm(websocket: WebSocket):
    await common_websocket_endpoint(websocket)

# Post endpoints
@Idle.post("/mainDisplay")
async def display_idle(item: IdleModel):
    """
    ## **IDLE MODEL** : 
    * **Message**  : The message number (Default = 1).
    * **DispTime** : The display Time (Default = 10 Seconds).
    * **Timer Image** : The timer between images (Default is 6 Seconds).
    """
    processed_data = {
        "message": item.message,
        "timerImage": item.timerIntervale,
    }
    return await broadcast_and_log(processed_data, "IdleModel")

@Stppd.post("/display/2")
async def display_stppd(item: STppd):
    """
    ## **Short Term Parker Price Display** : 
    * **Message**  : The message number = 2
    * **DispTime** : The display Time (Default = 10 Seconds).
    * **entryTime** : The entryTime passed as string.
    * **exitTime** : The exit passed as string.
    * **lenghtOfStay** : The length time passed as string.
    * **amount** : The amount to pay passed as string.
    * **currency** : The currency passed as string.
    * **licencePlate** : The licencePlate of the car passed as string.
    * **carImage** : The image of the car captured by the camera passed as base64 format.
    """
    processed_data = {
        "message": item.message,
        "DispTime": item.DispTime,
        "entryTime": item.entryTime,
        "exitTime": item.exitTime,
        "lenghtOfStay": item.lenghtOfStay,
        "amount": item.amount,
        "currency": item.currency,
        "licencePlate": item.licencePlate,
        "carImage": item.carImage,
    }
    return await broadcast_and_log(processed_data, "STppd")

@Estpgm.post("/display/3")
async def display_estpgm(item: EstpGm):
    """
    ## **Exit short term parker - Goodbye message** : 
    * **Message**  : The message number = 3 .
    * **DispTime** : The display Time (Default = 10 Seconds).
    * **paymentSuccess** : The payment success message passed as string.
    * **visitMessage** : The visit message passed as string.
    """
    processed_data = {
        "message": item.message,
        "DispTime": item.DispTime,
        "paymentSuccess": item.paymentSuccess,
        "visitMessage": item.visitMessage,
    }
    return await broadcast_and_log(processed_data, "EstpGm")

@Paygm.post("/display/4")
async def display_paygm(item: paygm):
    """
    ## **Pay as you go-GOODBYE Message** : 
    * **Message**  : The message number = 4.
    * **DispTime** : The display Time (Default = 10 Seconds).
    * **name** : The name of the customer passed as string.
    * **thankYouMessage** : The thank you message passed as string.
    * **licencePlate** : The licencePlate of the car passed as string.
    * **entryTime** : The entryTime passed as string.
    * **exitTime** : The exit passed as string.
    * **lenghtOfStay** : The length time passed as string.
    * **amountLabel** : The amount label passed as string.
    * **amount** : The amount to pay passed as string.
    * **currency** : The currency passed as string.
    * **carImage** : The image of the car captured by the camera passed as base64 format.
    """
    processed_data = {
        "message": item.message,
        "DispTime": item.DispTime,
        "name": item.name,
        "thankYouMessage": item.thankYouMessage,
        "licencePlate": item.licencePlate,
        "entryTime": item.entryTime,
        "exitTime": item.exitTime,
        "lenghtOfStay": item.lenghtOfStay,
        "amountLabel": item.amountLabel,
        "amount": item.amount,
        "currency": item.currency,
        "carImage": item.carImage,
    }
    return await broadcast_and_log(processed_data, "paygm")

@Psgm.post("/display/5")
async def display_psgm(item: psgm):
    """
    ## **Prebooking + Subscriber - GOODBYE Message** : 
    * **Message**  : The message number = 5.
    * **DispTime** : The display Time (Default = 10 Seconds).
    * **name** : The name of the customer passed as string.
    * **thankYouMessage** : The thank you message passed as string.
    * **licencePlate** : The licencePlate of the car passed as string.
    * **entryTime** : The entryTime passed as string.
    * **exitTime** : The exit passed as string.
    * **lenghtOfStay** : The length time passed as string.
    * **carImage** : The image of the car captured by the camera passed as base64 format.
    """
    processed_data = {
        "message": item.message,
        "DispTime": item.DispTime,
        "name": item.name,
        "thankYouMessage": item.thankYouMessage,
        "licencePlate": item.licencePlate,
        "entryTime": item.entryTime,
        "exitTime": item.exitTime,
        "lenghtOfStay": item.lenghtOfStay,
        "carImage": item.carImage,
    }
    return await broadcast_and_log(processed_data, "psgm")

