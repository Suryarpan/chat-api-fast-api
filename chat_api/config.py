from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Chat API"
    debug: bool = False
    app_host: str = "127.0.0.1"
    app_port: int = 5000
    jwt_secret: str = ""
    # DB creds
    mysql_host: str = "127.0.0.1"
    mysql_port: int = 3306
    mysql_user: str = ""
    mysql_password: str = ""
    mysql_database: str = "chat_api"
    mysql_pool: int = 10
    # APP actives
    user_active: bool = False

    model_config = SettingsConfigDict(env_prefix="CHAT_API_")
