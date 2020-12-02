import logging

from aiotg import Bot

import config

import workflows

logging.basicConfig(level=logging.INFO)

bot = Bot(api_token=config.API_TOKEN)

workflows.init(bot)

if __name__ == "__main__":
    # import asyncio
    # loop = asyncio.get_event_loop()
    # print(loop.run_until_complete(bot.get_me()))
    bot.run()
