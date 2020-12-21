import re
import json
import pydantic

from aiotg import Chat


from models import TelegramUser
from .db import get_db
from .bot import movers_chat


async def process_event(event):
    event = json.loads(event)
    if event["table"] == "temp_jobs":
        if event["row"]["status"] == "опрос чата":
            movers_chat.send_text(await get_jobs_msg(event["row"]["id"], 0))


async def get_jobs_msg(job_id, msg_type):
    async with (await get_db()).pool.acquire() as conn:
        return await conn.fetchrow(
            (
                """SELECT temp_messages.chat_message FROM temp_jobs JOIN temp_messages """
                """ON temp_messages.id = temp_jobs.messages_id WHERE temp_jobs.id = $1;"""
            ),
            job_id
        )


async def get_user_data_from_api(bot: Chat, user_id: int) -> TelegramUser:
    """
    retrieves user data and current avatar from telegram api
    """
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
    """
    inserts pydantic user model into database
    """
    async with (await get_db()).pool.acquire() as conn:
        _user = user.dict()
        avatar = _user.pop("profile_photo", None)
        #  save user data without avatar (pop it from dict if any),
        result = await conn.fetchrow(
            (
                """INSERT INTO bot_users (username, first_name, last_name, chat_id) """
                """VALUES ($1, $2, $3, $4) RETURNING bot_users.id"""
            ),
            *_user.values(),
        )
        saved_user_id = result.get("id")
        # but if there is one, save it separately
        if avatar:
            await conn.execute(
                """INSERT INTO avatars(bin_data, filename, user_id) VALUES ($1, $2, $3)""",
                *avatar.values(),
                saved_user_id,
            )


async def check_user_in_db(user_id: int):
    """
    checks if matching user_id (chat_id) database record exists
    """
    async with (await get_db()).pool.acquire() as conn:
        row = await conn.fetchrow("""SELECT bot_users.id FROM bot_users WHERE bot_users.chat_id = $1""", user_id)
        return row is not None


async def perform_registration(code: int, chat_id: int):
    async with (await get_db()).pool.acquire() as conn:
        mover = await conn.fetchrow("""SELECT * FROM temp_movers WHERE temp_movers.code = $1""", code)
        if mover is not None:
            bot_user = await conn.fetchrow("""SELECT * FROM bot_users WHERE chat_id = $1""", chat_id)
            await conn.execute(
                """UPDATE temp_movers SET bot_id = $1, status = $2 WHERE id = $3""",
                bot_user.get("id"),
                "готов к работе",
                mover.get("id"),
            )
        return mover


def emojize(s: str) -> str:
    EMOJIS = {"::hand_waves::": "\U0001F44B", "::confused::": "\U0001F615"}
    for template, value in EMOJIS.items():
        s = s.replace(template, value)
    return s


def escape_markdown(text: str, version: int = 2, entity_type: str = None) -> str:
    """
    Helper function to escape telegram markup symbols.
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
