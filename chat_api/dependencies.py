from functools import lru_cache

from chat_api.config import Settings


@lru_cache
def get_settings():
    return Settings()
