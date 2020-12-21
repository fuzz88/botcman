from aiotg import Bot
from multiprocessing import Process
import logging

import config
import workflows
from workflows import db_watcher

logging.basicConfig(level=logging.DEBUG)

bot = Bot(api_token=config.API_TOKEN)


def workflow_runner():
    workflows.init(bot)
    bot.run()


def db_watch_runner():
    db_watcher.run()


if __name__ == "__main__":
    Process(target=workflow_runner).start()
    Process(target=db_watch_runner).start()
