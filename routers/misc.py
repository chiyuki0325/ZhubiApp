# 外部模块
from fastapi import APIRouter, Depends
from fastapi.responses import Response

import magic

# 项目内部模块
from depends import (
    get_client
)

router = APIRouter(
    prefix='/misc',
)


@router.get('/media/{file_id}')
async def get_media(
        file_id: str,
        client=Depends(get_client)
):
    with client:
        file = await client.download_media(
            file_id,
            in_memory=True
        )
        file_as_bytes = bytes(file.getbuffer())
        # 使用 mag1c 判断文件类型
        mime_type = magic.from_buffer(file_as_bytes, mime=True)
        return Response(
            content=file_as_bytes,
            media_type=mime_type
        )
