from typing import Optional
from psycopg2 import errors
from account_controller.schemas import UserMeInfo, User
from database.db import cursor, connect


def add_user(username: str, hashed_password: str) -> bool:
    try:
        cursor.execute(
            'INSERT INTO USERS(username, hashed_password, admin) VALUES(%s, %s, false)',
            (username, hashed_password)
        )
        connect.commit()
        return True
    except errors.UniqueViolation:
        connect.rollback()
        return False


def update_tokens(username: str, access_token: str, refresh_token: str):
    cursor.execute(
        'UPDATE USERS SET access_token = %s, refresh_token = %s where username = %s',
        (access_token, refresh_token, username)
    )
    connect.commit()


def get_user_by_username(username: str) -> Optional[User]:
    cursor.execute('SELECT * FROM USERS WHERE username = %s', (username,))
    res = cursor.fetchone()

    if res:
        return User(**dict(zip(User.__match_args__, res)))


def get_user_info(user_id: int):
    cursor.execute("SELECT * FROM USERS WHERE id = %s", (user_id, ))
    res = cursor.fetchone()
    return UserMeInfo(id=res[0], username=res[1], is_admin=res[3])
