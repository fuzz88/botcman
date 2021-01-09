import re
import json
import pydantic

from aiotg import Chat

from models import TelegramUser
from .db import get_db
from .bot import movers_chat


async def process_event(event):
    # processes events from db_watcher.

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
            job_id,
        )


async def получить_инфу_об_отправителе_от_апи_телеграмма(bot: Chat, user_id: int) -> TelegramUser:
    # получаем на вход интерфейс для работы с Telegram API и идентификатор пользователя Телеграм.

    # получаем информацию о пользователе и ссылку на его аватарку.

    # скачиваем аватарку, собираем полученные данные в объект TelegramUser, валидируем, возвращаем.
    # если данные валидировать не удалось, то возвращаем None (ничего не возвращаем).

    # запрашиваем информацию о пользователе из телеграм апи.
    user_data = await Chat(bot, chat_id=user_id).get_chat()["result"]
    user_data["chat_id"] = user_id

    # проверяем наличие аватарки
    if user_data.get("photo", None) is not None:
        file = await bot.get_file(
            user_data["photo"]["small_file_id"]
        )  # запрашиваем версию аватарки с низким разрешением
        try:
            # пытаемся скачать
            async with bot.download_file(file["file_path"]) as response:
                filedata = await response.read()  # скачали,
                filename = file["file_path"].split("/")[1]
                user_data["profile_photo"] = {}  # подготавливаем к сохранению в базу данных
                user_data["profile_photo"]["bin_data"] = filedata
                user_data["profile_photo"]["filename"] = filename
        except Exception as e:
            print(e)
    try:
        # собираем в виде модели pydantic
        user = TelegramUser(**user_data)
        # и возвращаем
        return user
    except pydantic.ValidationError as e:
        # что-то не так с данными или моделью.
        print(e.json())


async def сохранить_инфу_о_пользователе_в_базу_данных(user: TelegramUser):
    # inserts pydantic model into database
    async with (await get_db()).pool.acquire() as conn:
        await user.save(conn)  # using dependency injection of asyncpg


async def есть_ли_у_нас_в_базе_такой_пользователь(id: int):
    # если пользователь есть в базе данных, то возвращаем True, иначе False.
    async with (await get_db()).pool.acquire() as conn:
        return (
            await conn.fetchrow("""SELECT bot_users.id FROM bot_users WHERE bot_users.chat_id = $1""", id) is not None
        )


async def выполнить_регистрацию_пользователя(code: int, chat_id: int) -> object:
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
    # helper function

    # escapes telegram markup symbols in string.

    # grabbed from internet.

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
