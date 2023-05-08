from aiogram import types, Dispatcher
from create_bot import dp


# @dp.message_handler()
async def support_function(message : types.Message):
    pass

def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(support_function)