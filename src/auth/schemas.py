from typing import Optional
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    manager_id: Optional[int] = None

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    password: str
    role_id: int
    manager_id: Optional[int] = None
