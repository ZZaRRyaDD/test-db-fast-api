from .database import Base
from sqlalchemy import Integer, String, Column, DateTime, func


class User(Base):
    """Model for each user."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    patronymic = Column(String)
    phone = Column(String(12), unique=True)
    email = Column(String, unique=True)
    passport_id = Column(String(4), unique=True)
    passport_series = Column(String(6), unique=True)
    created_at = Column(DateTime, default=func.now())