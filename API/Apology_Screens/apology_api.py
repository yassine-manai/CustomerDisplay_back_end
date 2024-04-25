from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from Manager.WebSocket import manager
from Models.items import *

app = FastAPI()
Paygam = APIRouter() #(9 + 10 + 11)


@Paygam.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            print(f"Received message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)



# S9 + S10 + S11-  Pay as you go-apology message
@Paygam.post("/display/messageId")
async def display_paygam(message :int , item: paygam):

    """
        ## Pay as you go-apology message:

**message = 9** 

            if the Message = 9 the processed_data send it is : 

                * message  : The message number (Default = 9).
                * DispTime : The display Time <1000ms = 1 second> (Default = 10 Seconds = 10000 ms).
                * apologyMessage : " We apologize, the license plate is not recognized or not found in our system !"
                * carImage : The image of the car captured by the camera passed as base64 format.

**message = 10** 

            if the Message = 10 the processed_data send it is : 

                * message  : The message number (message = 10).
                * DispTime : The display Time <1000ms = 1 second> (Default = 10 Seconds = 10000 ms).
                * apologyTitle : "We apologize !"
                * apologyDescription : "The license plate is not recognized or not found in our system!Our help desk cashier will help you to pay your fees."
                * carImage : The image of the car captured by the camera passed as base64 format.


                
**message = 11**  

            if the Message = 11 the processed_data send it is : 

                * message  : The message number (message = 11).
                * DispTime : The display Time <1000ms = 1 second> (Default = 10 Seconds = 10000 ms).
                * apologyTitle : "We apologize !"
                * apologyDescription : "The license plate is not recognized or not found in our system!"
                * helpDescription : "Our help desk cashier will help you to pay your fees."
                * carImage : The image of the car captured by the camera passed as base64 format.

    """
        
    try:

        if message == 9:
            processed_data = {
                "message": 9,
                "DispTime": item.DispTime,
                "apologyMessage": item.apologyMessage,
                "carImage": item.carImage,
            }

        if message == 10:
            processed_data = {
                "message": 10,
                "DispTime": item.DispTime,
                "apologyTitle": item.apologyTitle,
                "apologyDescription": item.apologyDescription,
                "carImage": item.carImage,
            }

        if message == 11:
            processed_data = {
                "message": 11,
                "DispTime": item.DispTime,
                "apologyTitle": item.apologyTitle,
                "apologyDescription": item.apologyDescription,
                "helpDescription": item.helpDescription,
                "carImage": item.carImage,
            }

        await manager.broadcast(processed_data)
        return processed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process request: {e}")
