import sqlalchemy
from typing import Optional
from pydantic import BaseModel, validator


class UserCredentials(BaseModel):
    username: str
    password: str


class API_User(BaseModel):
    id: int
    username: str
    password: str
    role: str


class AuthUser(BaseModel):
    username: str
    role: str


class Mover(BaseModel):
    id: Optional[int]
    fullname: str
    experience: int
    stamina: int
    reliability: int
    code: Optional[int]
    status: Optional[str]

    @validator("fullname")
    def must_contain_3_words(cls, v):
        if len(v.split(" ")) != 3:
            raise ValueError("должно состоять из трёх слов")
        return v.title()

    @validator("experience", "stamina", "reliability")
    def must_be_number(cls, v):
        if not (isinstance(v, int) and v >= 0):
            raise ValueError("должно быть положительным числом, или 0")
        return v


class Job(BaseModel):
    id: Optional[int]
    ext_id: int
    manager: str
    chat_message: str
    brigadier_message: str
    mover_message: str
    courier_message: str
    brigade: Optional[str]
    status: str


class JobInList(BaseModel):
    id: int
    ext_id: int
    manager: str
    brigadier: Optional[str]
    brigade: Optional[str]
    status: str
