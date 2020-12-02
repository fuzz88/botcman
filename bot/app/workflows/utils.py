import asyncpg
import pydantic

from aiotg import Bot, Chat

import config
from models import TelegramUser


async def get_user_data_from_api(bot: Bot, user_id: int) -> TelegramUser:
    """retrieves user data and current avatar from telegram api"""

    user_data = await Chat(bot, chat_id=user_id).get_chat()
    user_data = user_data["result"]
    user_data["chat_id"] = user_id

    if user_data.get("photo", None) is not None:
        file = await bot.get_file(user_data["photo"]["small_file_id"])
        try:
            async with bot.download_file(file["file_path"]) as response:
                filedata = await response.read()
                filename = file["file_path"].split("/")[1]
                user_data["profile_photo"] = {}
                user_data["profile_photo"]["bin_data"] = filedata
                user_data["profile_photo"]["filename"] = filename
        except Exception as e:
            print(e)
    try:
        user = TelegramUser(**user_data)
        return user
    except pydantic.ValidationError as e:
        print(e.json())


async def save_user_to_db(user: TelegramUser):
    """inserts pydantic user model into database"""

    conn = await asyncpg.connect(config.DATABASE_URL)
    q = (
        """INSERT INTO bot_users (username, first_name, last_name, chat_id) """
        """VALUES ($1, $2, $3, $4) RETURNING bot_users.id"""
    )

    _user = user.dict()
    avatar = _user.pop("profile_photo", None)
    #  save user data without avatar (pop it from dict if any),
    result = await conn.fetchrow(q, *_user.values())
    saved_user_id = result.get("id")
    # but if there is one, save it separately
    if avatar:
        q = """INSERT INTO avatars(bin_data, filename, user_id) VALUES ($1, $2, $3)"""
        await conn.execute(q, *avatar.values(), saved_user_id)

    await conn.close()


async def check_user_in_db(user_id: int):
    """checks if matching user_id (chat_id) database record exists"""

    conn = await asyncpg.connect(config.DATABASE_URL)

    q = """SELECT bot_users.id FROM bot_users WHERE bot_users.chat_id = $1"""
    row = await conn.fetchrow(q, user_id)

    await conn.close()

    return row is not None
