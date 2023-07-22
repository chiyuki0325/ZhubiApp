# 上下文变量

from pyrogram import Client
from database.database import Database
from datetime import datetime
from broadcaster import Broadcast

client: Client | None = None
db: Database | None = None
broadcast: Broadcast | None = None
token: str | None = None
token_last_used: datetime | None = None
