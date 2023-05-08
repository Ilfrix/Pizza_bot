from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from secret_values import token
bot = Bot(token=token)
dp = Dispatcher(bot)