from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Кнопки клавиатуры админы
button_load_pizza = KeyboardButton('/Загрузить')
button_delete_pizza = KeyboardButton('/Удалить')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(button_load_pizza)\
.add(button_delete_pizza)