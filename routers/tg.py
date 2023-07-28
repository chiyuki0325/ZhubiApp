# 外部模块
from fastapi import APIRouter, Depends

# 项目内部模块
from depends import use_da
from database.access import DatabaseAccess
from models.tg import *
from database.models import User, Chat, Message

__all__ = ['router']

router = APIRouter(
    prefix='/tg'
)

tg_user_router = APIRouter(
    prefix='/user'
)


@tg_user_router.get('/{user_id}/info')
async def tg_user_info(
        user_id: int,
        da: DatabaseAccess = Depends(use_da)
) -> TgUserInfoResponse:
    user: User | None = await da.get_user_by_id(user_id)
    if user is None:
        return TgUserInfoResponse(
            code=404,
            user=None
        )
    else:
        return TgUserInfoResponse(
            code=200,
            user=user.to_dict()
        )


router.include_router(
    tg_user_router
)
