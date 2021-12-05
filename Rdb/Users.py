from dataclasses import dataclass
from datetime import datetime
from .rdb import Cursor, conn


@dataclass()
class User:
    user_id: str
    password: str
    name: str
    email: str
    created_at: datetime
    updated_at: datetime
    status: int = 99


def get_user(user_id: str):
    with Cursor(dictionary=True) as cursor:
        sql = """
        SELECT * FROM Users
        WHERE user_id = %(user_id)s
        """.strip()
        cursor.execute(sql, {
            "user_id": user_id
        })
        rows = cursor.fetchall()
        if len(rows) == 1:
            return User(**rows[0])
        return None


def set_user(user_id: str, password: str, name: str, email: str):
    with Cursor() as cursor:
        sql = """
        INSERT INTO Users(`user_id`, `password`, `name`, `email`, `status`)
        VALUES (%(user_id)s, %(password)s, %(name)s, %(email)s, %(status)s)
        ON DUPLICATE KEY UPDATE `password` = %(password)s, `name` = %(name)s, `email` = %(email)s, `status` = %(status)s 
        """.strip()
        cursor.execute(sql, {
            "user_id": user_id,
            "password": password,
            "name": name,
            "email": email,
            "status": 99,
        })
    conn().commit()
    return
