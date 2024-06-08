from fastapi import FastAPI, Depends
from . import models, crud
from .database import engine
from .auth.models import User as AuthUser, Role
from .auth.base_config import fastapi_users, auth_backend, current_user
from .auth.schemas import UserRead, UserCreate

# Создаем приложение FastAPI
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    # Создание всех таблиц в базе данных
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
        await conn.run_sync(AuthUser.metadata.create_all)
        await conn.run_sync(Role.metadata.create_all)

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

@app.get("/protected-route", response_model=str)
async def protected_route(user=Depends(current_user)):
    return "Hello, world!"
