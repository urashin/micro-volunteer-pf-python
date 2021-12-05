from dataclasses import dataclass
from datetime import datetime
from .rdb import Cursor, conn


@dataclass()
class Session:
    session_id: str
    user_id: str
    created_at: datetime


def get_session(session_id: str) -> Session or None:
    with Cursor(dictionary=True) as cursor:
        sql = """
        SELECT * FROM Session
        WHERE session_id = %(session_id)s
        """.strip()
        cursor.execute(sql, {
            "session_id": session_id,
        })
        rows = cursor.fetchall()
        if len(rows) == 1:
            return Session(**rows[0])
        return None


def get_session_by_user_id(user_id: str) -> Session or None:
    with Cursor(dictionary=True) as cursor:
        sql = """
        SELECT * FROM Session
        WHERE user_id = %(user_id)s
        """.strip()
        cursor.execute(sql, {
            "user_id": user_id,
        })
        rows = cursor.fetchall()
        if len(rows) == 1:
            return Session(**rows[0])
        return None


def set_session(session_id: str, user_id: str):
    with Cursor() as cursor:
        sql = """
        INSERT INTO Session(`session_id`, `user_id`)
        VALUES (%(session_id)s, %(user_id)s)
        ON DUPLICATE KEY UPDATE `session_id` = %(session_id)s
        """.strip()
        cursor.execute(sql, {
            "user_id": user_id,
            "session_id": session_id,
        })
    conn().commit()
    return
