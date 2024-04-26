from venv import logger
from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from Manager.WebSocket import manager
from Models.items import *

app = FastAPI()

Idle = APIRouter() #Idle Model ADS Main Screen (1)
Stppd = APIRouter() #Short term parker-Price display (2)
Estpgm = APIRouter() #Exit short term parker - Goodbye message (3)
Paygm = APIRouter() #Pay as you go-GOODBYE Message (4) 
Psgm = APIRouter() #Prebooking + Subscriber - GOODBYE Message (5)



# WEB SOCKET + API N° 01 ----------------------------------------------------------------
@Idle.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"Received message: {data}")
            print()
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# S1- IDLE Model
@Idle.post("/display/1")
async def display_idle(item: IdleModel):

    """
        ## **IDLE MODEL** : 

        * **Message**  : The message number (Default = 1).
        * **DispTime** : The display Time (Default = 10 Seconds).
        * **Exit** : The pathImage is passed as base64 format.

    """

    try:
        processed_data = {
            "message": item.message,
            "DispTime": item.DispTime,
            "pathImage": item.pathImage,
        }
        await manager.broadcast(processed_data)
        return processed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process request: {e}")




# WEB SOCKET + API N° 02 ----------------------------------------------------------------
@Stppd.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"Received message: {data}")
            print()

    except WebSocketDisconnect:
        manager.disconnect(websocket)

# S2 - Short term parker-Price display
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
        * **pathImage** : The image of the car captured by the camera passed as base64 format.
    """
        
    try:
        processed_data = {
            "message": item.message,
            "DispTime": item.DispTime,
            "entryTime": item.entryTime,
            "exitTime": item.exitTime,
            "lenghtOfStay": item.lenghtOfStay,
            "amount": item.amount,
            "currency": item.currency,
            "licencePlate": item.licencePlate,
            "pathImage": item.pathImage,
        }
        await manager.broadcast(processed_data)
        return processed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process request: {e}")





# WEB SOCKET + API N° 03 ----------------------------------------------------------------
@Estpgm.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"Received message: {data}")
            print()

    except WebSocketDisconnect:
        manager.disconnect(websocket)

# S3 - Exit short term parker - Goodbye message
@Estpgm.post("/display/3")
async def display_Estpgm(item: EstpGm):

    """
        ## **Exit short term parker - Goodbye message** : 

        * **Message**  : The message number = 3 .
        * **DispTime** : The display Time (Default = 10 Seconds).
        * **paymentSuccess** : The payment success message passed as string.
        * **visitMessage** : The visit message passed as string.
    
    """
    try:
        processed_data = {
            "message": item.message,
            "DispTime": item.DispTime,
            "paymentSuccess": item.paymentSuccess,
            "visitMessage": item.visitMessage,
        }

        await manager.broadcast(processed_data)

        return processed_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process request: {e}")





# WEB SOCKET + API N° 04 ----------------------------------------------------------------
@Paygm.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"Received message: {data}")
            print()
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# S4 -  Pay as you go-GOODBYE Message
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
        * **amount** : The amount to pay passed as string.
        * **currency** : The currency passed as string.
        * **carImage** : The image of the car captured by the camera passed as base64 format.

    """
    try:
        processed_data = {
            "message": item.message,
            "DispTime": item.DispTime,
            "name": item.name,
            "thankYouMessage": item.thankYouMessage,
            "licencePlate": item.licencePlate,
            "entryTime": item.entryTime,
            "exitTime": item.exitTime,
            "lenghtOfStay": item.lenghtOfStay,
            "amount": item.amount,
            "currency": item.currency,
            "carImage": item.carImage,
        }
        await manager.broadcast(processed_data)
        return processed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process request: {e}")





# WEB SOCKET + API N° 05 ----------------------------------------------------------------
@Psgm.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"Received message: {data}")
            print()
        
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# S5 - Prebooking + Subscriber - GOODBYE Message
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
        
    try:
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
        await manager.broadcast(processed_data)
        return processed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process request: {e}")

