import importlib.metadata

from fastapi import FastAPI

from chat_api.dependencies import get_settings
from chat_api.health import router as health_router
from chat_api.users import router as user_router


def create_app():
    settings = get_settings()

    app = FastAPI(
        debug=settings.debug,
        title=settings.app_name,
        description="backend api for a chat application",
        version=importlib.metadata.version("chat-api"),
    )

    app.include_router(health_router)
    # all other routes
    if settings.user_active:
        app.include_router(user_router)

    return app
