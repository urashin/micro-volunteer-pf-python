from dataclasses import dataclass
from uuid import uuid4
from typing import Optional, List
import json
import redis
from .Redis import redis

key_prefix = "user"


@dataclass()
class User:
    user_id: str
    password: str
    name: str
    token: Optional[str] = None


def create_user(user_id: str, password: str, name: str) -> bool:
    token = uuid4().hex
    user = User(user_id, password, name)
    user.token = token

    # update/insert
    redis.set(f"{key_prefix}/{user_id}", json.dumps(user.__dict__, indent=2))
    return True


def get_user(user_id: str) -> User or None:
    # select one
    s = redis.get(f"{key_prefix}/{user_id}")
    if s is None:
        return None
    user = User(**json.loads(s))
    return user


def get_user_by_token(token: str) -> User or None:
    keys = redis.keys(f"{key_prefix}/*")
    users = [User(**json.loads(redis.get(key))) for key in keys]  # type: List[User]
    users = list(filter(lambda user: user.token == token, users))
    return users[0] if len(users) == 1 else None


def login(user_id: str, password: str) -> str:
    user = get_user(user_id)
    if user is None:
        raise Exception("user don't exist")
    if user.password != password:
        raise Exception("password incorrect")

    return user.token
