from venv import logger
from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from Manager.WebSocket import manager
from Models.items import *

app = FastAPI()


Payggm = APIRouter() #(6 + 7 + 8)


@Payggm.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"Received message: {data}")
            print()

    except WebSocketDisconnect:
        manager.disconnect(websocket)



# S6 + S7 + S8-  Pay as you go-GOODBYE Message
@Payggm.post("/display/message")
async def display_payggm(message :int , item: payggm):

    """
        ## **Pay as you go-GOODBYE Message** :

**message = 6** 

           if the Message = 6 the processed_data send it is : 

                * message  : The message number (Default = 6).
                * DispTime : The display Time (Default = 10 Seconds).
                * name : "Mr .. ... "
                * thankYouMessage : "You don’t have enough credit in your wallet"
                * licencePlate : "ABC123"
                * entryTime : "21-02-2024 14:36"
                * exitTime : "21-02-2024 17:36"
                * lenghtOfStay : "2 hours 31 minutes"
                * carImage : The image of the car captured by the camera passed as base64 format.

                
**message = 7** 

            if the Message = 7 the processed_data send it is : 

                * message : The message number (message = 7).
                * DispTime : The display Time (Default = 10 Seconds).
                * name : "Mr .. ... "
                * thankYouMessage : "You exceed your booking period"
                * licencePlate : "ABC123"
                * entryTime : "21-02-2024 14:36"
                * exitTime : "21-02-2024 17:36"
                * lenghtOfStay: "2 hours 31 minutes"
                * carImage : The image of the car captured by the camera passed as base64 format.

**message = 8** 

            if the Message = 8 the processed_data send it is : 

                * message  : The message number (message = 8).
                * DispTime : The display Time (Default = 10 Seconds).
                * name : "Mr .. ... ".
                * thankYouMessage : "Your subscription is expired".
                * licencePlate** : "ABC123".
                * entryTime : "21-02-2024 14:36".
                * exitTime : "21-02-2024 17:36".
                * lenghtOfStay : "2 hours 31 minutes".
                * carImage : The image of the car captured by the camera passed as base64 format.

    
    """
        
    try:

        if message == 6:
            processed_data = {
                "message": 6,
                "DispTime": item.DispTime,
                "name": item.name,
                "thankYouMessage": item.thankYouMessage,
                "licencePlate": item.licencePlate,
                "entryTime": item.entryTime,
                "exitTime": item.exitTime,
                "lenghtOfStay": item.lenghtOfStay,
                "currency": item.currency,
                "amount": item.amount,
                "carImage": item.carImage,
            }

        if message == 7:
            processed_data = {
                "message": 7,
                "DispTime": item.DispTime,
                "name": item.name,
                "thankYouMessage": item.thankYouMessage,
                "licencePlate": item.licencePlate,
                "entryTime": item.entryTime,
                "exitTime": item.exitTime,
                "lenghtOfStay": item.lenghtOfStay,
                "currency": item.currency,
                "amount": item.amount,
                "carImage": item.carImage,
            }

        if message == 8:
            processed_data = {
                "message": 8,
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
        logger.error(f"Error to process Request // 500 error")
        raise HTTPException(status_code=500, detail=f"Failed to process request: {e}")

