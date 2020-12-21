import config

from .utils import get_user_data_from_api, save_user_to_db, check_user_in_db, escape_markdown, emojize
from .data.loader import load

def init(bot):
    @bot.command(r"/start")
    async def greet_and_save_new_user(chat, match):
        await chat.send_text(escape_markdown(emojize(load("messages/on_start.md"))), **{"parse_mode": "MarkdownV2"})

        user_id = chat.sender["id"]
        known_user = await check_user_in_db(user_id)

        if not known_user:
            user = await get_user_data_from_api(bot, user_id)
            await save_user_to_db(user)
