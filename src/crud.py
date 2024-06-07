from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from . import models, schemas, database, auth
from .telegram import send_message
from .auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/api",
    tags=["API"]
)

def get_user_by_username(username: str, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/authenticate_user")
def authenticate_user(username: str, password: str, db: Session = Depends(database.get_db)):
    user = get_user_by_username(username, db)
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return user

@router.post("/create_user", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password, role_id=user.role_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/create_role", response_model=schemas.Role)
def create_role(role: schemas.RoleCreate, db: Session = Depends(database.get_db)):
    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.get("/roles", response_model=list[schemas.Role])
def get_roles(db: Session = Depends(database.get_db)):
    return db.query(models.Role).all()

@router.post("/create_request_log", response_model=schemas.RequestLog)
def create_request_log(request: schemas.RequestLogCreate, user_id: int, db: Session = Depends(database.get_db)):
    db_request_log = models.RequestLog(
        user_id=user_id,
        bottoken=request.bottoken,
        chatid=request.chatid,
        message=request.message,
        response=request.response
    )
    db.add(db_request_log)
    db.commit()
    db.refresh(db_request_log)
    return db_request_log

@router.post("/send_message", response_model=schemas.RequestLog)
def send_message_and_log(request: schemas.RequestLogCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    # Отправляем сообщение в Telegram
    response = send_message(request.bottoken, request.chatid, request.message)
    # Сохраняем запрос и ответ в базу данных
    db_request_log = models.RequestLog(
        user_id=current_user.id,
        bottoken=request.bottoken,
        chatid=request.chatid,
        message=request.message,
        response=response
    )
    db.add(db_request_log)
    db.commit()
    db.refresh(db_request_log)
    return db_request_log
