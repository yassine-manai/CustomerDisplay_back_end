import configparser
from dotenv import load_dotenv
import os

load_dotenv()

def add_default_section_header(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    if not content.startswith('['):
        with open(file_path, 'w') as file:
            file.write('[DEFAULT]\n' + content)

config_file_path = 'config/config.ini'
add_default_section_header(config_file_path)

config = configparser.ConfigParser()
config.read(config_file_path)

APP_IP =  str(os.getenv("APP_IP")) 
APP_PORT =  int(os.getenv("APP_PORT")) 

SERVER_IP =  str(os.getenv("SERVER_IP")) 
SERVER_PORT =  int(os.getenv("SERVER_PORT"))

POS_IP =  str(os.getenv("POS_IP")) 
POS_PORT =  int(os.getenv("POS_PORT"))
POS_API = str(os.getenv("POS_API"))

OPERATOR_ID =  int(os.getenv("OPERATOR_ID")) 
ZR_ID =  int(os.getenv("ZR_ID")) 
SAVE_PATH =  str(os.getenv("SAVE_PATH"))
    

