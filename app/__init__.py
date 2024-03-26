import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
HOST = os.getenv('HOST')
DB = os.getenv('DB')
DBUSER = os.getenv('DBUSER')
PASSWORD = os.getenv('PASSWORD')
ROOT = int(os.getenv('ROOT'))
PORT = os.getenv('PORT')
loop = asyncio.get_event_loop()