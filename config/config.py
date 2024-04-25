import configparser
from dotenv import load_dotenv
import os
load_dotenv()

config = configparser.ConfigParser()
config.read('config/config.ini')

APP_IP =  str(os.getenv("APP_IP")) if os.getenv("APP_IP") else config.getint('APP', 'APP_IP',fallback='127.0.0.1')
APP_PORT =  int(os.getenv("APP_PORT")) if os.getenv("APP_PORT") else config.getint('APP', 'APP_PORT',fallback=8100)


    