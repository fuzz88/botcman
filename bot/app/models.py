from typing import Optional

import pydantic


class TelegramUser(pydantic.BaseModel):
    # используем для валидации данных от API Телеграма.
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    chat_id: int
    profile_photo: Optional[dict]

    async def save(self, conn):
        user = self.dict()
        avatar = user.pop("profile_photo", None)
        if avatar is not None:
            await conn.execute(
                """INSERT INTO avatars(bin_data, filename, user_id) VALUES ($1, $2, $3)""",
                # saving "profile_photo"
                *avatar.values(),
                (
                    await conn.fetchrow(
                        """INSERT INTO bot_users (username, first_name, last_name, chat_id) """
                        """VALUES ($1, $2, $3, $4) RETURNING bot_users.id""",
                        *user.values(),
                    )
                ).get("id"),
            )


# class Mover(pydantic.BaseModel):
#     # используем для валидации данных из БД

#     # хотя пока не используем.
#     id: int
#     fullname: str
#     experience: int
#     stamina: int
#     activity: int
#     code: Optional[int]
