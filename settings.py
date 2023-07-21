from pydantic_settings import BaseSettings
from typing import (
    Optional as Opt,
    Literal
)


class Settings(BaseSettings):
    telegram_api_id: int
    telegram_api_hash: str

    api_host: Opt[str] = 'localhost'
    api_port: Opt[int] = 8080

    auth_method: Opt[Literal['password', 'webauthn']] = 'password'
    # password, webauthn (todo)

    password: Opt[str] = 'nm$l'

    # 在关闭浏览器后，token 多久会失效
    token_expire_minutes: Opt[int] = 1

    postgresql_host: Opt[str] = 'localhost'
    postgresql_port: Opt[int] = 5432
    postgresql_user: Opt[str] = 'zhubiapp'
    postgresql_password: Opt[str] = ''
    postgresql_database: Opt[str] = 'zhubiapp'

    loglevel: Opt[str] = 'INFO'

    frontend_files: Opt[str] = 'web/dist'

    cors_allowed_origins: Opt[str] = '*'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_prefix = 'zhubiapp_'
        case_sensitive = False


settings = Settings()

app_version: str = '0.0.1'
