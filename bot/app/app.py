import logging

from aiotg import Bot

import config

import workflows

logging.basicConfig(level=logging.DEBUG)

bot = Bot(api_token=config.API_TOKEN)

workflows.init(bot)

if __name__ == "__main__":
    bot.run()
