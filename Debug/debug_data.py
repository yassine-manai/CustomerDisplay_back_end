from fastapi import FastAPI, APIRouter
from globalvars.globals import local_data

app = FastAPI()
debug_local_data = APIRouter() 

@debug_local_data.get("/debug/global_infos")
def get_local_data():
    return local_data