from typing import Optional

import pydantic


class TelegramUser(pydantic.BaseModel):
    """ we need some user information from telegram api"""

    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    chat_id: int
    profile_photo: Optional[dict]


class Mover(pydantic.BaseModel):
    id: int
    fullname: str
    experience: int
    stamina: int
    activity: int
    code: Optional[int]
