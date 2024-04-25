# main.py

import uvicorn

from fastapi import FastAPI
import websockets
from API.Apology_Screens.apology_api import *
from API.Display.display_api import *
from API.Location_Data.location_api import *
from API.Payment_Screens.payment_api import *

from config.config import APP_PORT



app = Fastapp = FastAPI(
    title="E-POS : ADS Backend",
    version="1.0.0",
)

app.include_router(LocationData, tags=["Location Data"])
app.include_router(Idle, tags=["Payment Screens"])
app.include_router(Stppd, tags=["Payment Screens"])
app.include_router(Estpgm, tags=["Payment Screens"])
app.include_router(Paygm, tags=["Payment Screens"])
app.include_router(Psgm, tags=["Payment Screens"])
app.include_router(Payggm, tags=["Payment Screens - GOODBYE Messages"])
app.include_router(Paygam, tags=["Pay As You Go Screens - Apology Messages"])


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()
    
    try:
        websockets.add(websocket)
        print("WebSocket connection established")

        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")

            for ws in websockets:
                if ws != websocket and ws.client_state != 3:
                    try:
                        await ws.send_text(data)
                    except:
                        websockets.remove(ws)

    except WebSocketDisconnect:
        websockets.remove(websocket)
        print("WebSocket disconnected")

    except Exception as e:
        print(f"WebSocket error: {e}") 
        

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=APP_PORT, reload=True)














