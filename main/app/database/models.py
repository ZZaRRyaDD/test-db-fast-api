from sqlalchemy import Column, DateTime, Integer, String, func

from .database import Base


class User(Base):
    """Model for each user."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128))
    surname = Column(String(128))
    phone = Column(String(12), unique=True)
    email = Column(String(32), unique=True)
    passport_id = Column(String(4), unique=True)
    passport_series = Column(String(6), unique=True)
    created_at = Column(DateTime, default=func.now())
