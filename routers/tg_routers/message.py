# 外部模块
from fastapi import APIRouter, Depends, HTTPException

# 项目内部模块
from depends import use_da, verify_token
from database.access import DatabaseAccess
from models.tg import *
from database.models import User, Chat, Message

router = APIRouter(
    prefix='/message'
)


@router.get('/by_tg_id/{chat_id}/{tg_id}')
async def tg_message_by_tg_id(
        da: DatabaseAccess = Depends(use_da),
        verified: bool = Depends(verify_token),
        chat_id: int = None,
        tg_id: int = None
) -> TgMessageResponse:
    message: Message = await da.get_message_by_tg_id(chat_id, tg_id)
    if message is None:
        raise HTTPException(
            status_code=404,
            detail="消息不存在"
        )
    return TgMessageResponse(
        message=message.to_dict()
    )


@router.get('/by_db_id/{db_id}')
async def tg_message_by_db_id(
        da: DatabaseAccess = Depends(use_da),
        verified: bool = Depends(verify_token),
        db_id: int = None
) -> TgMessageResponse:
    message: Message = await da.get_message_by_db_id(db_id)
    if message is None:
        raise HTTPException(
            status_code=404,
            detail="消息不存在"
        )
    return TgMessageResponse(
        message=message.to_dict()
    )
