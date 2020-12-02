from .utils import get_user_data_from_api, save_user_to_db, check_user_in_db


def init(bot):
    @bot.command(r"(.+)")
    async def save_new_user(chat, message):
        user_id = chat.sender["id"]
        user = await get_user_data_from_api(bot, user_id)
        known_user = await check_user_in_db(user_id)

        if not known_user:
            await save_user_to_db(user)
