import logging

from aiogram import Bot, Dispatcher, executor

import config

from workflows import log_new_bot_user

logging.basicConfig(level=logging.INFO)


bot = Bot(token=config.API_TOKEN)
disp = Dispatcher(bot)

log_new_bot_user.init(disp)


if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True)
