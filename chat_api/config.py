from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    debug: bool = False
    # DB creds
    mysql_user: str
    mysql_password: str
    mysql_database: str
    # APP actives
    user_active: bool = False

    model_config = SettingsConfigDict(env_prefix="CHAT_API_")
