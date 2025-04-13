import uvicorn

from chat_api.dependencies import get_settings

settings = get_settings()

if __name__ == "__main__":
    log_level = "info"
    if settings.debug:
        log_level = "debug"
    config = uvicorn.Config(
        "chat_api:create_app", factory=True, port=8000, log_level=log_level, ws="none"
    )
    server = uvicorn.Server(config)
    server.run()
