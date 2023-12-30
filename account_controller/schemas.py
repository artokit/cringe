import datetime
from dataclasses import dataclass
from pydantic import BaseModel


class UserRegisterSchema(BaseModel):
    username: str
    password: str


class UserRegisterResponseSuccess(BaseModel):
    time_register_user: datetime.datetime


class LoginUserSchema(BaseModel):
    username: str
    password: str


class LoginSuccessSchema(BaseModel):
    status: int
    access_token: str


class UserMeInfo(BaseModel):
    id: int
    username: str
    is_admin: bool


@dataclass
class User:
    id: int
    username: str
    hashed_password: str
    admin: bool
    access_token: str
    refresh_token: str
