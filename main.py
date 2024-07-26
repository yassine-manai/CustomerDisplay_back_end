import uvicorn
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from API.Apology_Screens.apology_api import *
from API.Display.display_api import *
from API.Payment_Screens.payment_api import *
from API.imageLoader.image_api import Banner_Images, Main_Images
from API.Timer.ScreenTimer import *
from API.Location_Data.get_pos_info import UpdateLocData
from API.Location_Data.get_pos_info import get_data_from_pos
from Debug.debug_data import debug_local_data

from config.config import APP_PORT, CRON
from config.log_config import logger


app = FastAPI(
    title="Customer Display : Backend",
    version="1.0.0",
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all the routers
#app.include_router(LocationData, tags=["Location Data"])
#app.include_router(FooterData, tags=["Footer Data"])


app.include_router(UpdateLocData, tags=["Location Data"])
app.include_router(Idle, tags=["Main Screen"])
app.include_router(Stppd, tags=["Payment Screens"])
app.include_router(Estpgm, tags=["Payment Screens"])
app.include_router(Paygm, tags=["Payment Screens"])
app.include_router(Psgm, tags=["Payment Screens"])
app.include_router(Payggm, tags=["Payment Screens - GOODBYE Messages"])
app.include_router(Paygam, tags=["Pay As You Go Screens - Apology Messages"])
app.include_router(Main_Images, tags=["Ads Images"])
app.include_router(Banner_Images, tags=["Ads Images"])
app.include_router(GetTimersData, tags=["Ads Timers"])
#app.include_router(UpdateTimersData, tags=["Ads Timers"])
app.include_router(UpdateAdsData, tags=["Ads Manager"])
app.include_router(debug_local_data, tags=["DEBUG"])

async def scheduled_tasks():
    while True:
        logger.info("---- Fetching data from POS ----")
        resp=get_data_from_pos()
        
        if not resp:
            logger.error(" * * *   ERROR WHILE CALLing POS Default   * * * ")
            
        await asyncio.sleep(2)
        
        logger.info("Fetching ads data")
        update_images_from_control()
        
        await asyncio.sleep(CRON*3600)
        logger.info(CRON)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(scheduled_tasks())


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=APP_PORT, reload=True)