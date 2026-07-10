from app.database import Base
from sqlalchemy import Column, Integer, String


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    year = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # We store the current refresh token here so we can:
    # 1. Check it's still valid when the user tries to refresh
    # 2. "Revoke" it by clearing this field (e.g. on logout)
    refresh_token = Column(String, nullable=True)
