from pydantic import BaseModel
from typing import Optional


class RoleBase(BaseModel):
    name: str
    can_view_all_requests: Optional[bool] = False
    can_view_own_requests: Optional[bool] = True
    can_manage_users: Optional[bool] = False


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True


class RequestLogBase(BaseModel):
    bottoken: str
    chatid: str
    message: str


class RequestLogCreate(RequestLogBase):
    pass


class RequestLog(RequestLogBase):
    id: int
    user_id: int
    response: Optional[str]

    class Config:
        from_attributes = True
