from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional

T = TypeVar('T')


@dataclass(frozen=True)
class BaseResponse(Generic[T]):
    status: int
    message: str
    response: T


@dataclass(frozen=True)
class SendTextRequest:
    sns_id: str
    message: str


@dataclass(frozen=True)
class SendTextResponse:
    pass


@dataclass(frozen=True)
class SendLocationRequest:
    sns_id: str
    title: str
    address: str
    latitude: float
    longitude: float


@dataclass(frozen=True)
class SendLocationResponse:
    pass


@dataclass(frozen=True)
class LocationMessageDto:
    title: str
    address: str
    latitude: float
    longitude: float


@dataclass(frozen=True)
class LabelValueDto:
    label: str
    text: str


@dataclass(frozen=True)
class ActionButtonDto:
    text: str
    link: str


@dataclass(frozen=True)
class ActionsDto:
    primary: Optional[ActionButtonDto] = None
    secondary: Optional[ActionButtonDto] = None


@dataclass(frozen=True)
class ActionMessageDto:
    title: str
    actions: ActionsDto
    details: list[LabelValueDto] = field(default_factory=list)


@dataclass(frozen=True)
class SendRequestVolunteerRequest:
    sns_id: str
    location_message: LocationMessageDto
    action_message: ActionMessageDto

    @classmethod
    def from_json(cls, contents: dict):
        # map `location_message`
        location_message = contents["location_message"]
        location_message_dto = LocationMessageDto(**location_message)

        # map `action_message`
        action_message = contents["action_message"]

        def _action_or_none(key):
            return action_message["actions"][key] if key in action_message["actions"] else None

        actions = {
            "primary": _action_or_none("primary"),
            "secondary": _action_or_none("secondary"),
        }
        actions = {k: ActionButtonDto(**v) for k, v in actions.items() if v is not None}
        actions_dto = ActionsDto(**actions)
        details: list[LabelValueDto] = list(map(lambda _: LabelValueDto(**_), action_message["details"]))
        action_message_dto = ActionMessageDto(action_message["title"], actions_dto, details)

        # return instance
        return cls(contents["sns_id"], location_message_dto, action_message_dto)


@dataclass(frozen=True)
class SendRequestVolunteerResponse:
    pass
