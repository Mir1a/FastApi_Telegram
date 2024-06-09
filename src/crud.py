from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from .models import RequestLog
from .auth.models import Role, User
from .auth.schemas import UserCreate, UserRead as UserSchema
from .schemas import RequestLogCreate, RequestLog as RequestLogSchema, RoleCreate, Role as RoleSchema
from .database import get_async_session
from .telegram import send_message
from .auth.base_config import current_user
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/api",
    tags=["API"]
)


@router.get("/users", response_model=List[UserSchema])
async def get_all_users(db: AsyncSession = Depends(get_async_session)):
    users = await db.execute(select(User))
    return users.scalars().all()


@router.post("/create_user", response_model=UserSchema)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        role_id=user.role_id,
        email=user.email,
        manager_id=user.manager_id
    )
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


@router.post("/send_message", response_model=RequestLogSchema)
async def send_message_and_log(
    request: RequestLogCreate,
    current_user: User = Depends(current_user),
    db: AsyncSession = Depends(get_async_session)
):
    response = send_message(request.bottoken, request.chatid, request.message)
    db_request_log = RequestLog(
        user_id=current_user.id,
        bottoken=request.bottoken,
        chatid=request.chatid,
        message=request.message,
        response=response
    )
    db.add(db_request_log)
    await db.commit()
    await db.refresh(db_request_log)
    return db_request_log


@router.get("/my_logs", response_model=List[RequestLogSchema])
async def get_my_logs(current_user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(RequestLog).where(RequestLog.user_id == current_user.id))
    return result.scalars().all()


@router.get("/subordinate_logs", response_model=List[RequestLogSchema])
async def get_subordinate_logs(current_user: User = Depends(current_user),
                               db: AsyncSession = Depends(get_async_session)):
    await db.refresh(current_user, ["role"])

    if current_user.role.name != 'manager':
        raise HTTPException(status_code=403, detail="Not authorized to view subordinate logs")

    result = await db.execute(
        select(RequestLog).where(RequestLog.user_id.in_(
            select(User.id).where(User.manager_id == current_user.id)
        ))
    )
    return result.scalars().all()


@router.get("/all_logs", response_model=List[RequestLogSchema])
async def get_all_logs(current_user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    await db.refresh(current_user, ["role"])

    if current_user.role.name != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized to view all logs")

    result = await db.execute(select(RequestLog))
    return result.scalars().all()
