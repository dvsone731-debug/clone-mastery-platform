from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="free")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LessonProgress(Base):
    __tablename__ = "lesson_progress"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    lesson_id = Column(Integer)
    completed = Column(Boolean, default=False)
