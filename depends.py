# 外部模块
from fastapi import Request
from pyrogram import Client

# 程序内模块
from database.access import DatabaseAccess


async def create_da(request: Request):
    async with request.app.state.db.async_session() as session:
        async with session.begin():
            yield DatabaseAccess(session)


async def get_client(request: Request) -> Client:
    return request.app.state.client
