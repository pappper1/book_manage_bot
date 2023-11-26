from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data.config import BOT_TOKEN
from utils.postgres.commands_to_db import Database

#Создание объектов бота, диспетчера и базы данных
db = Database()
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

bot_commands = [BotCommand(command="/start", description="Запустить бота")]
