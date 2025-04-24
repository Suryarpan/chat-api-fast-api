from fastapi import APIRouter

from chat_api.dependencies import DBDep

router = APIRouter(prefix="/user", tags=["user"])

from .types import UserModel


@router.get("", response_model=UserModel)
async def get_users(db: DBDep) -> dict[str, str]:
    a = {"some": "thing"}
    res = (await db.read("select 1 AS idv", {}))[0]
    a.update(res)
    return a
