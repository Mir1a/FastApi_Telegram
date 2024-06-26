from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from .auth.models import User
from .database import Base


class RequestLog(Base):
    __tablename__ = "request_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    bottoken = Column(String)
    chatid = Column(String)
    message = Column(Text)
    response = Column(Text)

    user = relationship("User", back_populates="request_logs")


User.request_logs = relationship("RequestLog", back_populates="user")
