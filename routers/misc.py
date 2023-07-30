# 外部模块
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from loguru import logger
import magic

# 项目内部模块
from depends import (
    use_client
)

router = APIRouter(
    prefix='/misc',
)


@router.get('/media/{file_id}')
async def get_media(
        file_id: str,
        client=Depends(use_client)
):
    with client:
        file = await client.download_media(
            file_id,
            in_memory=True
        )
        file_as_bytes = bytes(file.getbuffer())
        # 使用 mag1c 判断文件类型
        mime_type = magic.from_buffer(file_as_bytes, mime=True)
        logger.info(
            f'获取文件 {file_id}，类型 {mime_type}'
        )
        return Response(
            content=file_as_bytes,
            media_type=mime_type,
            headers={
                'Cache-Control': 'max-age=31536000'  # 一年
            }
        )
