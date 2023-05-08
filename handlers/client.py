from aiogram import types, Dispatcher
from create_bot import dp, bot

# @dp.message_handler(commands=['start'])
async def start_work(message : types.Message):
    await bot.send_message(message.from_user.id, 'Добро пожаловать! Я бот для пиццерии!')

# @dp.message_handler(commands=['Режим_работы'])
async def pizza_time(message : types.Message):
    await bot.send_message(message.from_user.id, 'Ежедневно с 10:00 до 23:00')

# @dp.message_handler(commands=['Адрес'])
async def pizza_place(message : types.Message):
    await bot.send_message(message.from_user.id, 'г. Москва, ул. Полярная д.10, стр. 1')

# @dp.message_handler(commands=['Телефон'])
async def pizza_phone(message : types.Message):
    await bot.send_message(message.from_user.id, '+7 495 845-05-25')

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(start_work, commands = ['start'])
    dp.register_message_handler(pizza_time, commands = ['Режим_работы'])
    dp.register_message_handler(pizza_place, commands = ['Адрес'])
    dp.register_message_handler(pizza_phone, commands = ['Телефон'])