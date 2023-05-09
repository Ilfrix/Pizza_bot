from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from secret_values import admin_id
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ID = None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()

# @dp.message_handler(commands=['модератор'])
async def check_admin(message : types.Message):
    global ID
    ID = message.from_user.id
    if ID in admin_id:
        await bot.send_message(message.from_user.id, 'Что надо, хозяин?', reply_markup=admin_kb.button_case_admin)
        print(f'Пользователь {message.from_user.full_name} вошел как Администратор')
    else:
        await bot.send_message(message.from_user.id, 'Ошибка прав доступа')
# Начало диалога загрузки новго пункта меню
# @dp.message_handler(commands=['Загрузить'], state = None)
async def start(message : types.Message):
    if ID in admin_id:
        await FSMAdmin.photo.set()
        await message.reply('Загрузите фото')
    else:
        await message.reply('Ошибка прав доступа!!')

# Ловим первый ответ и записываем в словарь
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_pizza_photo(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply('Теперь введите название')

# Ловим второй ответ
# @dp.message_handler(state=FSMAdmin.name)
async def load_pizza_name(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply('Введите описание')

# Ловим третий ответ
# @dp.message_handler(state=FSMAdmin.description)
async def load_pizza_description(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.reply('Теперь укажите цену')

# Ловим последний ответ и используем полученные данные
# @dp.message_handler(state=FSMAdmin.price)
async def load_pizza_price(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)

    await sqlite_db.sql_add_command(state)

    await state.finish()
    await bot.send_message(message.from_user.id, 'Успешно! Продолжим?', reply_markup=admin_kb.button_case_admin)

# @dp.message_handler(state='*', commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message : types.Message, state : FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')

# @dp.message_handler(Text(equals='отмена', ignore_case=True))
async def cancel_text_handler(message : types.Message):
    await message.reply('OK')

# @dp.message_handler(commands=['Удалить'])
async def delete_pizza(message : types.Message):
    read = await sqlite_db.sql_read2()
    for ret in read:
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[-1]}')
        await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                               add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))

# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_pizza(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_pizza(callback_query.data.replace('del', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del", "")} удалена.', show_alert=True)

# Регистрация хендлеров
def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(start, commands=['Загрузить'], state=None)
    dp.register_message_handler(load_pizza_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_pizza_name, state=FSMAdmin.name)
    dp.register_message_handler(load_pizza_description, state=FSMAdmin.description)
    dp.register_message_handler(load_pizza_price, state=FSMAdmin.price)
    dp.register_message_handler(cancel_handler, state='*', commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(check_admin, commands=['модератор'])
    dp.register_message_handler(cancel_text_handler, Text(equals='отмена', ignore_case=True))
    dp.register_message_handler(delete_pizza, commands=['Удалить'])
    dp.register_callback_query_handler(del_callback_pizza, lambda x: x.data and x.data.startswith('del '))
