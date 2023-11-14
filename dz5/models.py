from typing import Optional
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///task8/db8.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": True})

Base = declarative_base()
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db8 = SessionLocal()


class TaskBase(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, nullable=False)
    title = Column(String(80), nullable=False)
    description = Column(String(80), nullable=False)
    status = Column(String(80), nullable=False)
    is_del = Column(Boolean, nullable=False)


class Task(BaseModel):
    task_id: int
    title: Optional[str] = None
    description: str
    status: Optional[str] = None
