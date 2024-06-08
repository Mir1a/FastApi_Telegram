from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from ..database import Base

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    can_view_all_requests = Column(Boolean, default=False)
    can_view_own_requests = Column(Boolean, default=True)
    can_manage_users = Column(Boolean, default=False)
    users = relationship("User", back_populates="role")

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey('roles.id'))
    hashed_password = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    role = relationship("Role", back_populates="users")
