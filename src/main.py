import asyncio
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, Depends
from . import models, crud
from .database import engine
from .auth.models import User as AuthUser, Role
from .auth.base_config import fastapi_users, auth_backend, current_user
from .auth.schemas import UserRead, UserCreate
from .telegram import start_bot

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
        await conn.run_sync(AuthUser.metadata.create_all)
        await conn.run_sync(Role.metadata.create_all)
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(max_workers=1)
    loop.run_in_executor(executor, start_bot)

app.include_router(crud.router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
