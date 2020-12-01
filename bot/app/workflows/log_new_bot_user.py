from aiogram import types
from .utils import get_user_data, save_user_to_db


def init(disp):
    @disp.message_handler()
    async def log_new_user(message: types.Message):

        user = await get_user_data(disp, message)
        await save_user_to_db(user)
