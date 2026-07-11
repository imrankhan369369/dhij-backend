from app.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime


class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    offering = Column(String)
    bio = Column(String)





class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # We store the current refresh token here so we can:
    # 1. Check it's still valid when the user tries to refresh
    # 2. "Revoke" it by clearing this field (e.g. on logout)
    refresh_token = Column(String, nullable=True)
    role = Column(String, default="user")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    provider_id = Column(Integer, ForeignKey("providers.id"))
    scheduled_time = Column(DateTime)
    meeting_link = Column(String, nullable=True)
    status = Column(String, default="pending")
