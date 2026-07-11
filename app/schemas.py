from pydantic import BaseModel
from typing import Optional

# ==========================================
# STUDENT SCHEMAS
# ==========================================




# ==========================================
# USER / AUTH SCHEMAS
# ==========================================

class UserSignup(BaseModel):
    username: str
    password: str


# What we send back after signup — notice: NO password, NO hashed_password
# This is the whole point of a response schema: control exactly what leaves your API
class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


# What we send back after a successful login
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


# What the client sends to get a new access token
class RefreshRequest(BaseModel):
    refresh_token: str


class ProviderCreate(BaseModel):
    name: str
    offering: str
    bio: str


class ProviderResponse(BaseModel):
    id: int
    name: str
    offering: str
    bio: str

    class Config:
        from_attributes = True


from datetime import datetime


class BookingCreate(BaseModel):
    provider_id: int
    scheduled_time: datetime


class BookingResponse(BaseModel):
    id: int
    user_id: int
    provider_id: int
    scheduled_time: datetime
    meeting_link: Optional[str] = None
    status: str

    class Config:
        from_attributes = True