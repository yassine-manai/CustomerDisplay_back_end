from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from Manager.WebSocket import manager
from Models.items import *

app = FastAPI()

LocationData = APIRouter() #This is for location data
Idle = APIRouter() #Idle Model (1)
Stppd = APIRouter() #(2)
Estpgm = APIRouter() #(3)
Paygm = APIRouter() #(4) 
Psgm = APIRouter() #(5)
Payggm = APIRouter() #(6 + 7 + 8)
Paygam = APIRouter() #(9 + 10 + 11)


@Paygm.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            print(f"Received message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)


#Location Data
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


# S1- IDLE Model
@Idle.post("/display/1")
async def display_idle(item: IdleModel):

    """
        ## **IDLE MODEL** : 

        * **Message**  : The message number (Default = 1).
        * **DispTime** : The display Time <1000ms = 1 second> (Default = 10 Seconds = 10000 ms).
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

# S2 - Short term parker-Price display
@Stppd.post("/display/2")
async def display_stppd(item: STppd):
    
    """
        ## **Short Term Parker Price Display** : 

        * **Message**  : The message number (Default = 2).
        * **DispTime** : The display Time <1000ms = 1 second> (Default = 10 Seconds = 10000 ms).
        * **entryTime** : The entryTime passed as string.
        * **exitTime** : The exit passed as string.
        * **length** : The length time passed as string.
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
            "length": item.length,
            "amount": item.amount,
            "currency": item.currency,
            "licencePlate": item.licencePlate,
            "pathImage": item.pathImage,
        }
        await manager.broadcast(processed_data)
        return processed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process request: {e}")


# S3 - Exit short term parker - Goodbye message
@Estpgm.post("/display/3")
async def display_Estpgm(item: EstpGm):

    """
        ## **Exit short term parker - Goodbye message** : 

        * **Message**  : The message number (Default = 4).
        * **DispTime** : The display Time <1000ms = 1 second> (Default = 10 Seconds = 10000 ms).
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


# S4 -  Pay as you go-GOODBYE Message
@Paygm.post("/display/4")
async def display_paygm(item: paygm):

    """
        ## **Pay as you go-GOODBYE Message** : 

        * **Message**  : The message number (Default = 4).
        * **DispTime** : The display Time <1000ms = 1 second> (Default = 10 Seconds = 10000 ms).
        * **name** : The name of the customer passed as string.
        * **thankYouMessage** : The thank you message passed as string.
        * **licencePlate** : The licencePlate of the car passed as string.
        * **entryTime** : The entryTime passed as string.
        * **exitTime** : The exit passed as string.
        * **length** : The length time passed as string.
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
            "length": item.length,
            "amount": item.amount,
            "currency": item.currency,
            "carImage": item.carImage,
        }
        await manager.broadcast(processed_data)
        return processed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process request: {e}")



# S5 - Prebooking + Subscriber - GOODBYE Message
@Psgm.post("/display/5")
async def display_psgm(item: psgm):

    """
        ## **Prebooking + Subscriber - GOODBYE Message** : 

        * **Message**  : The message number (Default = 5).
        * **DispTime** : The display Time <1000ms = 1 second> (Default = 10 Seconds = 10000 ms).
        * **name** : The name of the customer passed as string.
        * **thankYouMessage** : The thank you message passed as string.
        * **licencePlate** : The licencePlate of the car passed as string.
        * **entryTime** : The entryTime passed as string.
        * **exitTime** : The exit passed as string.
        * **length** : The length time passed as string.
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
            "length": item.length,
            "carImage": item.carImage,
        }
        await manager.broadcast(processed_data)
        return processed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process request: {e}")



# S6 + S7 + S8-  Pay as you go-GOODBYE Message
@Payggm.post("/display/message")
async def display_payggm(message :int , item: payggm):

    """
        ## **Pay as you go-GOODBYE Message** :

            if the Message = 6 the processed_data send it is : 

                * message  : The message number (Default = 6).
                * DispTime : The display Time <1000ms = 1 second> (Default = 10 Seconds = 10000ms).
                * name : "Mr .. ... "
                * thankYouMessage : "You don’t have enough credit in your wallet"
                * licencePlate : "ABC123"
                * entryTime : "21-02-2024 14:36"
                * exitTime : "21-02-2024 17:36"
                * length : "2 hours 31 minutes"
                * carImage : The image of the car captured by the camera passed as base64 format.


            if the Message = 7 the processed_data send it is : 

                * message : The message number (message = 7).
                * DispTime : The display Time <1000ms = 1 second> (Default = 10 Seconds = 10000ms).
                * name : "Mr .. ... "
                * thankYouMessage : "You exceed your booking period"
                * licencePlate : "ABC123"
                * entryTime : "21-02-2024 14:36"
                * exitTime : "21-02-2024 17:36"
                * length : "2 hours 31 minutes"
                * carImage : The image of the car captured by the camera passed as base64 format.

            if the Message = 8 the processed_data send it is : 

                * message  : The message number (message = 8).
                * DispTime : The display Time <1000ms = 1 second> (Default = 10 Seconds = 10000ms).
                * name : "Mr .. ... ".
                * thankYouMessage : "Your subscription is expired".
                * licencePlate** : "ABC123".
                * entryTime : "21-02-2024 14:36".
                * exitTime : "21-02-2024 17:36".
                * length : "2 hours 31 minutes".
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
                "length": item.length,
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
                "length": item.length,
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
                "length": item.length,
                "amount": item.amount,
                "currency": item.currency,
                "carImage": item.carImage,
            }

        await manager.broadcast(processed_data)
        return processed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process request: {e}")



# S9 + S10 + S11-  Pay as you go-apology message
@Paygam.post("/display/messageId")
async def display_paygam(message :int , item: paygam):

    """
        ## ** Pay as you go-apology message** :

            if the Message = 9 the processed_data send it is : 

                * message  : The message number (Default = 9).
                * DispTime : The display Time <1000ms = 1 second> (Default = 10 Seconds = 10000 ms).
                * apologyMessage : " We apologize, the license plate is not recognized or not found in our system !"
                * carImage : The image of the car captured by the camera passed as base64 format.


            if the Message = 10 the processed_data send it is : 

                * message  : The message number (message = 10).
                * DispTime : The display Time <1000ms = 1 second> (Default = 10 Seconds = 10000 ms).
                * apologyTitle : "We apologize !"
                * apologyDescription : "The license plate is not recognized or not found in our system!Our help desk cashier will help you to pay your fees."
                * carImage : The image of the car captured by the camera passed as base64 format.

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
