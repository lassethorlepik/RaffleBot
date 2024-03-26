from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app import API_TOKEN

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=storage)