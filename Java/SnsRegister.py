import json
from dataclasses import dataclass
import pprint
import requests
import config


@dataclass()
class SnsRegisterResponse:
    token: str


def sns_register(sns_id: str, sns_type: int) -> SnsRegisterResponse:
    res = requests.get(
        url=f"{config.java_host}/v1/user/sns_register",
        headers={
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "sns_id": sns_id,
            "sns_type": sns_type,
        })
    )

    pprint.pprint(res.json())

    return SnsRegisterResponse(**res.json())
