# 外部模块
from fastapi import APIRouter, Depends, HTTPException

# 项目内部模块
from depends import use_da, verify_token
from database.access import DatabaseAccess
from models.tg import *
from database.models import User, Chat, Message

__all__ = ['router']

router = APIRouter(
    prefix='/tg'
)

tg_chat_router = APIRouter(
    prefix='/chat'
)


@tg_chat_router.get('/list')
async def tg_chat_list(
        da: DatabaseAccess = Depends(use_da),
        verified: bool = Depends(verify_token)
) -> TgChatListResponse:
    chats: list[Chat] = await da.get_all_chats()
    return TgChatListResponse(
        chats=[
            chat.to_dict() for chat in chats
        ]
    )


tg_user_router = APIRouter(
    prefix='/user'
)


@tg_user_router.get('/{user_id}/info')
async def tg_user_info(
        user_id: int,
        da: DatabaseAccess = Depends(use_da),
        verified: bool = Depends(verify_token)
) -> TgUserInfoResponse:
    user: User | None = await da.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail='用户不存在'
        )
    else:
        return TgUserInfoResponse(
            user=user.to_dict()
        )


for sub_router in [
    tg_user_router,
    tg_chat_router
]:
    router.include_router(
        sub_router
    )
