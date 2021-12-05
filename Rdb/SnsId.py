from dataclasses import dataclass
from datetime import datetime
from .rdb import Cursor, conn


@dataclass()
class SnsId:
    user_id: str
    created_at: datetime
    sns_id: str
    sns_type: int = 1


def get_sns_id(sns_id: str) -> SnsId or None:
    with Cursor(dictionary=True) as cursor:
        sql = """
        SELECT * FROM SnsId
        WHERE sns_id = %(sns_id)s
        """.strip()
        cursor.execute(sql, {
            "sns_id": sns_id,
        })
        rows = cursor.fetchall()
        if len(rows) == 1:
            return SnsId(**rows[0])
        return None


def get_all_sns_id() -> list[SnsId]:
    with Cursor(dictionary=True) as cursor:
        sql = """
        SELECT * FROM SnsId
        """.strip()
        cursor.execute(sql, {})
        rows = cursor.fetchall()
        return [SnsId(**row) for row in rows]


def get_sns_id_by_user_id(user_id: str) -> SnsId or None:
    with Cursor(dictionary=True) as cursor:
        sql = """
        SELECT * FROM SnsId
        WHERE user_id = %(user_id)s
        """.strip()
        cursor.execute(sql, {
            "user_id": user_id,
        })
        rows = cursor.fetchall()
        if len(rows) == 1:
            return SnsId(**rows[0])
        return None


def set_sns_id(sns_id: str, user_id: str):
    with Cursor() as cursor:
        sql = """
        INSERT INTO SnsId(`sns_id`, `sns_type`, `user_id`, `created_at`)
        VALUES (%(sns_id)s, %(sns_type)s, %(user_id)s, %(created_at)s)
        ON DUPLICATE KEY UPDATE `sns_id` = %(sns_id)s
        """.strip()
        cursor.execute(sql, {
            "user_id": user_id,
            "sns_id": sns_id,
            "sns_type": 1,
            "created_at": datetime.now(),
        })
    conn().commit()
    return
