from pydantic import BaseModel
from typing import (
    Dict,
    Optional as Opt
)


class TgUserInfoResponse(BaseModel):
    code: int
    user: Opt[Dict | None]
