# 外部模块
from fastapi import APIRouter, Depends

# 项目内部模块
from depends import use_da, verify_token
from database.access import DatabaseAccess
from models.tg import *
from database.models import User, Chat, Message

router = APIRouter(
    prefix='/chat'
)


@router.get('/list')
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
