from dataclasses import dataclass
from typing import List
import json
import redis
from .Redis import redis
from . import Users

key_prefix = "sns"


@dataclass()
class SnsId:
    user_id: str
    sns_id: str
    sns_type: str


def insert_sns(user_id: str, sns_id: str, sns_type: str) -> bool:
    sns = SnsId(
        user_id=user_id,
        sns_id=sns_id,
        sns_type=sns_type,
    )

    # update/insert
    redis.set(f"{key_prefix}/{user_id}", json.dumps(sns.__dict__, indent=2))
    return True


def get_user_by_sns_id(sns_id: str, sns_type: str) -> Users or None:
    sns_ids = get_all_sns_by_type(sns_type)
    sns_ids = list(filter(lambda s: s.sns_id == sns_id, sns_ids))
    return sns_ids[0] if len(sns_ids) == 1 else None


def get_all_sns_by_type(sns_type: str) -> List[SnsId]:
    """
    指定したSNS_TYPEのsns_idをすべて取得する
    :param sns_type:
    :return: List[SnsId]
    """
    keys = redis.keys(f"{key_prefix}/*")
    sns_ids = [SnsId(**json.loads(redis.get(key))) for key in keys]  # type: List[SnsId]
    sns_ids = list(filter(lambda s: s.sns_type == sns_type, sns_ids))
    return sns_ids
