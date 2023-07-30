# 外部模块
from fastapi import Request, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pyrogram import Client
from datetime import datetime

# 程序内模块
from database.access import DatabaseAccess
import context
from settings import settings

__all__ = ['use_da', 'use_client', 'verify_token']


async def use_da(request: Request):
    async with request.app.state.db.async_session() as session:
        async with session.begin():
            yield DatabaseAccess(session)


async def use_client(request: Request) -> Client:
    return request.app.state.client


security = HTTPBearer()


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> bool:
    if credentials.scheme.lower() != 'bearer':
        raise HTTPException(
            status_code=401,
            detail="无效的验证方式"
        )
    if credentials.credentials != context.token:
        raise HTTPException(
            status_code=401,
            detail="token 不正确"
        )
    if (datetime.now() - context.token_last_used).total_seconds() / 60 > settings.token_expire_minutes:
        raise HTTPException(
            status_code=401,
            detail="登录已过期"
        )

    context.token_last_used = datetime.now()
    return True
