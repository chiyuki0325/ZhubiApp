from pydantic import BaseModel
from typing import Optional as Opt


class UserLoginMethodResponse(BaseModel):
    method: str


class UserLoginPasswordRequest(BaseModel):
    password_hash: str


class UserLoginPasswordResponse(BaseModel):
    code: int
    token: Opt[str]
