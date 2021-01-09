from aiotg import Bot, Chat

import config

bot = Bot(api_token=config.API_TOKEN)

# чат, в котором тусуются муверы.
movers_chat = Chat(bot, chat_id=config.MOVERS_CHAT_ID)
