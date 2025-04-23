from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Chat API"
    debug: bool = False
    app_host: str
    app_port: int
    # DB creds
    mysql_host: str = "127.0.0.1"
    mysql_port: int = 3306
    mysql_user: str = ""
    mysql_password: str = ""
    mysql_database: str = "chat_api"
    # APP actives
    user_active: bool = False

    model_config = SettingsConfigDict(env_prefix="CHAT_API_")
