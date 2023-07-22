# 外部模块
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from loguru import logger

# 项目内部模块
from depends import (
    get_client
)
from settings import settings
from models.user import *
import utils
import context
from datetime import datetime

router = APIRouter(
    prefix='/user',
)

login_router = APIRouter(
    prefix='/login',
)


@login_router.get('/method')
async def user_login_method() -> UserLoginMethodResponse:
    # 获取登录方式
    return UserLoginMethodResponse(
        method=settings.auth_method
    )


@login_router.post('/password')
async def user_login_password(
        request: UserLoginPasswordRequest
) -> UserLoginPasswordResponse:
    # 密码登录
    if request.password_hash == utils.calculate_password_hash(
            settings.password
    ):
        # 密码正确
        context.token = utils.generate_token()
        context.token_last_used = datetime.now()
        return UserLoginPasswordResponse(
            code=200,
            token=context.token
        )
    else:
        return UserLoginPasswordResponse(
            code=403,
            token=None
        )


@router.post('/validate')
async def user_validate(
        request: UserValidateRequest
) -> UserValidateResponse:
    if request.token == context.token:
        if (datetime.now() - context.token_last_used).total_seconds() / 60 < settings.token_expire_minutes:
            return UserValidateResponse(
                code=200,
                valid=True
            )
    return UserValidateResponse(
        code=403,
        valid=False
    )


router.include_router(
    login_router
)
