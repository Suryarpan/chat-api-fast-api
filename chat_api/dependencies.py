from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from chat_api.common import MysqlDB
from chat_api.config import Settings


@lru_cache
def get_settings():
    return Settings()


@lru_cache
def get_dbcon():
    from . import mysql_db

    return mysql_db


SettingsDep = Annotated[Settings, Depends(get_settings)]
DBDep = Annotated[MysqlDB, Depends(get_dbcon)]
