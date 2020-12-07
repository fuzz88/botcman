import re
import functools
import asyncpg
import pydantic

from aiotg import Chat
from async_lru import alru_cache

import config
from models import TelegramUser


@alru_cache
async def get_user_data_from_api(bot: Chat, user_id: int) -> TelegramUser:
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


@alru_cache
async def check_user_in_db(user_id: int):
    """checks if matching user_id (chat_id) database record exists"""

    conn = await asyncpg.connect(config.DATABASE_URL)

    q = """SELECT bot_users.id FROM bot_users WHERE bot_users.chat_id = $1"""
    row = await conn.fetchrow(q, user_id)

    await conn.close()

    return row is not None


async def perform_registration(code: int, chat_id: int):
    conn = await asyncpg.connect(config.DATABASE_URL)

    q = """SELECT * FROM temp_movers WHERE temp_movers.code = $1"""
    mover = await conn.fetchrow(q, code)

    q = """SELECT * FROM bot_users WHERE chat_id = $1"""
    bot_user = await conn.fetchrow(q, chat_id)

    q = """UPDATE temp_movers SET bot_id = $1, status = $2 WHERE id = $3"""
    await conn.execute(q, bot_user.get("id"), "готов к работе", mover.get("id"))

    await conn.close()
    return mover


def emojize(s: str) -> str:
    EMOJIS = {"::hand_waves::": "\U0001F44B", "::confused::": "\U0001F615"}
    for template, value in EMOJIS.items():
        s = s.replace(template, value)
    return s


def escape_markdown(text: str, version: int = 2, entity_type: str = None) -> str:
    """
    Helper function to escape telegram markup symbols.
    Args:
        text (:obj:`str`): The text.
        version (:obj:`int` | :obj:`str`): Use to specify the version of telegrams Markdown.
            Either ``1`` or ``2``. Defaults to ``1``.
        entity_type (:obj:`str`, optional): For the entity types ``PRE``, ``CODE`` and the link
            part of ``TEXT_LINKS``, only certain characters need to be escaped in ``MarkdownV2``.
            See the official API documentation for details. Only valid in combination with
            ``version=2``, will be ignored else.
    """
    if int(version) == 1:
        escape_chars = r"_*`["
    elif int(version) == 2:
        if entity_type in ["pre", "code"]:
            escape_chars = r"\`"
        elif entity_type == "text_link":
            escape_chars = r"\)"
        else:
            escape_chars = r"[]()~`>#+-=|{}.!"
    else:
        raise ValueError("Markdown version must be either 1 or 2!")

    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)
