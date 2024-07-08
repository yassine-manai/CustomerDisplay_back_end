import uvicorn
import time

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from API.Apology_Screens.apology_api import *
from API.Display.display_api import *
from API.Footer.footer_api import FooterData
from API.Location_Data.location_api import *
from API.Payment_Screens.payment_api import *
from API.imageLoader.image_api import Banner_Images, Main_Images
from API.Timer.ScreenTimer import TimersData
from API.Location_Data.location_loader import UpdateLocData
from API.imageLoader.images_load import fetch_and_save_images

from config.config import APP_PORT
from config.log_config import logger



app = Fastapp = FastAPI(
    title="E-POS : ADS Backend",
    version="1.0.0",
    detail="Server Work Correctly"
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)




app.include_router(LocationData, tags=["Location Data"])

app.include_router(UpdateLocData, tags=["Location Data"])
app.include_router(FooterData, tags=["Footer Data"])
app.include_router(Idle, tags=["Main Screen"])
app.include_router(Stppd, tags=["Payment Screens"])
app.include_router(Estpgm, tags=["Payment Screens"])
app.include_router(Paygm, tags=["Payment Screens"])
app.include_router(Psgm, tags=["Payment Screens"])
app.include_router(Payggm, tags=["Payment Screens - GOODBYE Messages"])
app.include_router(Paygam, tags=["Pay As You Go Screens - Apology Messages"])

app.include_router(Main_Images, tags=["Imported Images"])
app.include_router(Banner_Images, tags=["Imported Images"])

app.include_router(TimersData, tags=["Timers"])

logger.info(" Server Work Correctly ")


#fetch_and_save_images()      

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=APP_PORT, reload=True)














