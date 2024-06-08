from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from .models import RequestLog
from .auth.models import Role, User
from .schemas import RoleCreate, Role as RoleSchema, UserCreate, User as UserSchema, RequestLogCreate, RequestLog as RequestLogSchema
from .database import get_async_session
from .telegram import send_message
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/api",
    tags=["API"]
)

@router.post("/create_user", response_model=UserSchema)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password, role_id=user.role_id)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.post("/create_role", response_model=RoleSchema)
async def create_role(role: RoleCreate, db: AsyncSession = Depends(get_async_session)):
    db_role = Role(**role.dict())
    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    return db_role

@router.get("/roles", response_model=List[RoleSchema])
async def get_roles(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Role))
    return result.scalars().all()

@router.post("/create_request_log", response_model=RequestLogSchema)
async def create_request_log(request: RequestLogCreate, user_id: int, db: AsyncSession = Depends(get_async_session)):
    db_request_log = RequestLog(
        user_id=user_id,
        bottoken=request.bottoken,
        chatid=request.chatid,
        message=request.message,
        response=request.response
    )
    db.add(db_request_log)
    await db.commit()
    await db.refresh(db_request_log)
    return db_request_log

@router.post("/send_message", response_model=RequestLogSchema)
async def send_message_and_log(request: RequestLogCreate, db: AsyncSession = Depends(get_async_session)):
    response = send_message(request.bottoken, request.chatid, request.message)
    db_request_log = RequestLog(
        user_id=request.user_id,
        bottoken=request.bottoken,
        chatid=request.chatid,
        message=request.message,
        response=response
    )
    db.add(db_request_log)
    await db.commit()
    await db.refresh(db_request_log)
    return db_request_log

@router.get("/logs", response_model=List[RequestLogSchema])
async def get_logs(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(RequestLog))
    return result.scalars().all()
