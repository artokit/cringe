from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from psycopg2 import errors
from pydantic import BaseModel

from database.db import cursor, connect


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    hashed_password: str
    access_token: str


class SafeUser(BaseModel):
    username: str


class UpdateInfo(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: str | None = None


ALGORITHM = "HS256"
SECRET_KEY = '280ddac5faf437668a119086fdb4955468b087101eebaa8280f2057d74463cc5'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def add_user(username: str, hashed_password: str) -> bool:
    try:
        cursor.execute('INSERT INTO USERS VALUES(%s, %s, null)', (username, hashed_password))
        connect.commit()
        return True
    except errors.UniqueViolation:
        connect.rollback()
        return False


def update_access_token(username: str, access_token: str):
    cursor.execute('UPDATE USERS SET access_token = %s where username = %s', (access_token, username))
    connect.commit()


def get_user_by_username(username: str) -> Optional[User]:
    cursor.execute('SELECT * FROM USERS WHERE username = %s', (username,))
    res = cursor.fetchone()

    if res:
        return User(username=username, hashed_password=res[1], access_token=res[2])


def update_user(old_username: str, new_username: str, password: str):
    h = get_password_hash(password)
    cursor.execute(
        'UPDATE USERS SET username = %s, hashed_password = %s where username = %s',
        (new_username, h, old_username)
    )
    connect.commit()
