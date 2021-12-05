from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar('T')


@dataclass(frozen=True)
class BaseResponse(Generic[T]):
    status: int
    message: str
    response: T


@dataclass(frozen=True)
class UserCreateRequest:
    user_id: str
    password: str
    name: str


@dataclass(frozen=True)
class UserCreateResponse:
    user_id: str
    token: str


@dataclass(frozen=True)
class LoginRequest:
    user_id: str
    password: str


@dataclass(frozen=True)
class LoginResponse:
    token: str


@dataclass(frozen=True)
class LoginInfoRequest:
    token: str


@dataclass(frozen=True)
class LoginInfoResponse:
    user_id: str
    name: str
    email: str


@dataclass(frozen=True)
class LinkSnsRequest:
    token: str
    sns_id: str


@dataclass(frozen=True)
class LinkSnsResponse:
    pass


@dataclass(frozen=True)
class SnsGreetRequest:
    token: str
    message: str


@dataclass(frozen=True)
class SnsGreetResponse:
    pass


