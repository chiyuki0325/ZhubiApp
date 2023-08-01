from pydantic import BaseModel
from typing import (
    List,
    Dict,
    Optional as Opt
)


class TgUserInfoResponse(BaseModel):
    user: Dict


class TgChatListResponse(BaseModel):
    chats: List[Dict]


class TgMessageResponse(BaseModel):
    message: Dict
