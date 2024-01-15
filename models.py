from datetime import datetime, timezone
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    alt_name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String)
    is_active = Column(Boolean, default=True)
    joined_on = Column(DateTime, default=datetime.now(timezone.utc))


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(Integer, ForeignKey("users.id"))
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    created_on = Column(DateTime, default=datetime.now(timezone.utc))

class Salaries(Base):
    __tablename__ = "salaries"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer)
    received_by = Column(Integer, ForeignKey("users.id"))
    details = Column(String)
    is_approved = Column(Boolean, default=False)
    date_received = Column(DateTime, default=datetime.now(timezone.utc))
