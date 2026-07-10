from pydantic import BaseModel
from typing import Optional


# ==========================================
# STUDENT SCHEMAS
# ==========================================

# What the client must SEND when creating a student
class StudentCreate(BaseModel):
    name: str
    age: int
    year: str


# What the client can SEND when updating (all fields optional)
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


# What the API SENDS BACK for a student
# Having this separate from StudentCreate matters once fields differ
# (e.g. if you add "created_at" or hide internal fields later)
class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    year: str

    class Config:
        # This tells Pydantic: "it's OK to build this schema
        # from a SQLAlchemy object, not just a plain dict"
        from_attributes = True


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
