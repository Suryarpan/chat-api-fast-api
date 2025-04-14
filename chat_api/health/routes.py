from typing import Annotated

from fastapi import APIRouter, Depends

from chat_api.config import Settings
from chat_api.dependencies import get_settings

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health_check(settings: Annotated[Settings, Depends(get_settings)]):
    return {"status": "ok", "config": settings.model_dump()}
