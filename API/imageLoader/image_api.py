import os
import base64
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from Models.items import ImageData
from config.log_config import logger

app = FastAPI()

Banner_Images = APIRouter() 
Main_Images = APIRouter() 

IMAGES_PATH = os.path.abspath("/mnt/c/test_api/POSAD/API/imageLoader/images")

def get_images(prefix: str) -> List[ImageData]:
    logger.info(f"Images path: {IMAGES_PATH}")
    
    images_data = []

    if os.path.exists(IMAGES_PATH):
        for filename in os.listdir(IMAGES_PATH):
            if filename.startswith(prefix):
                image_path = os.path.join(IMAGES_PATH, filename)
                with open(image_path, "rb") as img_file:
                    b64_string = base64.b64encode(img_file.read()).decode('utf-8')
                    file_extension = os.path.splitext(filename)[1][1:]  
                    mime_type = f"image/{file_extension}"
                    b64_with_extension = f"data:{mime_type};base64,{b64_string}"
                    images_data.append(ImageData(filename=filename, base64=b64_with_extension))
        logger.info(f"Found {len(images_data)} images with prefix '{prefix}'")
    else:
        logger.error(f"Images path does not exist: {IMAGES_PATH}")
    
    return images_data

@Banner_Images.get("/get_banner", response_model=List[ImageData])
def get_banner():
    return get_images("banner")

@Main_Images.get("/get_mainScreen", response_model=List[ImageData])
def get_mainScreen():
    return get_images("main")

