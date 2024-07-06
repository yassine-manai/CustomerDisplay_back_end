import os
import base64
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from Models.items import ImageData

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


Banner_Images = APIRouter() 
Main_Images = APIRouter() 


IMAGES_PATH = os.path.abspath("/mnt/c/test_api/POSAD/functions/images")


def get_images(prefix: str) -> List[ImageData]:
    print(f"Images path: {IMAGES_PATH}")
    
    images_data = []

    if os.path.exists(IMAGES_PATH):
        for filename in os.listdir(IMAGES_PATH):
            if filename.startswith(prefix):
                image_path = os.path.join(IMAGES_PATH, filename)
                with open(image_path, "rb") as img_file:
                    b64_string = base64.b64encode(img_file.read()).decode('utf-8')
                    file_extension = os.path.splitext(filename)[1][1:]  # Get the file extension without the dot
                    mime_type = f"image/{file_extension}"
                    b64_with_extension = f"data:{mime_type};base64,{b64_string}"
                    images_data.append(ImageData(filename=filename, base64=b64_with_extension))
    
    return images_data


@Banner_Images.get("/get_banner", response_model=List[ImageData])
def get_banner():
    return get_images("bs")

@Main_Images.get("/get_mainScreen", response_model=List[ImageData])
def get_mainScreen():
    return get_images("ms")

