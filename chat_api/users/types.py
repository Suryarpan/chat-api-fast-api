from pydantic import BaseModel


class UserModel(BaseModel):
    some: str
    idv: int
