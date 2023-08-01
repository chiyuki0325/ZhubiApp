# 外部模块
from fastapi import APIRouter, Depends, HTTPException

# 项目内部模块
from depends import use_da, verify_token
from database.access import DatabaseAccess
from models.tg import *
from database.models import User, Chat, Message

router = APIRouter(
    prefix='/user'
)


@router.get('/{user_id}/info')
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
