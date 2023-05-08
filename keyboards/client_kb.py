from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('/Режим_работы')
b2 = KeyboardButton('/Адрес')
b3 = KeyboardButton('/Телефон')
b4 = KeyboardButton('/Меню')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(b1).insert(b2).insert(b3).insert(b4)
