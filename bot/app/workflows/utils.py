import databases
from sqlalchemy import sql
from aiogram import types
import aiohttp
import config
from models import BotUser, BotUserWithoutAvatar, bot_users, avatars
import pydantic

database = databases.Database(config.DATABASE_URL)


async def get_user_data(disp, message: types.Message):
    user_data = {
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "chat_id": message.chat.id,
        "profile_photo": {},
    }

    photos = await message.from_user.get_profile_photos()

    if photos.total_count >= 1:

        avatar_id = photos.photos[0][0].file_id

        file = await disp.bot.get_file(avatar_id)

        file_url = (
            f"https://api.telegram.org/file/" f"bot{config.API_TOKEN}/{file.file_path}"
        )
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(file_url) as response:
                    file_data = await response.read()
                    filename = file.file_path.split("/")[1]
                    user_data["profile_photo"]["bin_data"] = file_data
                    user_data["profile_photo"]["filename"] = filename
        except Exception as e:
            print(e)

    try:
        user = BotUser(**user_data)
        return user
    except pydantic.ValidationError as e:
        print(e.json())


async def save_user_to_db(user):

    if await is_known_user(user):
        return

    await database.connect()

    user_query = bot_users.insert()
    result = await database.execute(
        query=user_query,
        values=BotUserWithoutAvatar(**user.dict()).dict(),
    )
    if user.profile_photo != {}:
        ava_query = avatars.insert()
        result = await database.execute(
            query=ava_query, values=user.profile_photo | {"user_id": result}
        )

    await database.disconnect()


async def is_known_user(user):

    await database.connect()

    q = sql.select([bot_users.c.id]).where(bot_users.c.chat_id == user.chat_id)
    result = await database.fetch_one(query=q)

    await database.disconnect()
    return result is not None
