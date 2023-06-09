from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from data_base import sqlite_db

# @dp.message_handler(commands=['start'])
async def start_work(message : types.Message):
    print(f"Пользователь {message.from_user.full_name} - id {message.from_user.id}")
    greeting = "Добро пожаловать! Я бот для пиццерии!\n\
Вот что я могу\n\
/сайт - здесь вы сможете найти наш сайт\n\
/режим_работы - укажу рабочее время\n\
/адрес - расскажу где мы находимся\n\
/телефон - подскажу как связаться\n\
/меню - продемонстрирую меню\n\
/модератор - для администраторов"
    await bot.send_message(message.from_user.id, greeting, reply_markup=kb_client)

# @dp.message_handler(commands=['Режим_работы'])
async def pizza_time(message : types.Message):
    await bot.send_message(message.from_user.id, 'Ежедневно с 10:00 до 23:00')

# @dp.message_handler(commands=['Адрес'])
async def pizza_place(message : types.Message):
    await bot.send_message(message.from_user.id, 'г. Москва, ул. Полярная д.10, стр. 1')

# @dp.message_handler(commands=['Телефон'])
async def pizza_phone(message : types.Message):
    await bot.send_message(message.from_user.id, '+7 495 845-05-25')

# @dp.message_handler(commands=['Меню'])
async def pizza_menu(message : types.Message):
    await sqlite_db.sql_read_pizza(message)

# @dp.message_handler(commands=['Сайт', 'site'])
async def site_pizza(message : types.Message):
    await bot.send_message(message.from_user.id, 'https://allopizza.su')

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(start_work, commands = ['start'])
    dp.register_message_handler(pizza_time, commands = ['Режим_работы'])
    dp.register_message_handler(pizza_place, commands = ['Адрес'])
    dp.register_message_handler(pizza_phone, commands = ['Телефон'])
    dp.register_message_handler(pizza_menu, commands=['Меню'])
    dp.register_message_handler(site_pizza, commands=['Сайт', 'site'])