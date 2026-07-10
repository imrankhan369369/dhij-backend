from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User as UserModel
from app.schemas import UserSignup, UserResponse, Token, RefreshRequest
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)

# APIRouter is a "mini FastAPI app" - we define routes on it here,
# then plug the whole router into the main app in main.py.
# prefix="/auth" means every route below automatically starts with /auth
# tags=["Authentication"] just groups these nicely in the /docs page
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Tells FastAPI where to send users to get a token (used for the /docs "Authorize" button)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# ==========================================
# DEPENDENCY: get the currently logged-in user from a token
# ==========================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserModel:
    payload = decode_token(token)

    if payload is None or payload.get("type") != "access":
        # Either the token failed to decode, OR someone passed a
        # refresh token where an access token was expected
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    username = payload.get("sub")
    user = db.query(UserModel).filter(UserModel.username == username).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# ==========================================
# ROUTES
# ==========================================

@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(user: UserSignup, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(
        UserModel.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = UserModel(
        username=user.username,
        hashed_password=hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(
        UserModel.username == form_data.username
    ).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})

    # Save the refresh token in the DB so we can validate / revoke it later
    user.refresh_token = refresh_token
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=Token)
def refresh_access_token(request: RefreshRequest, db: Session = Depends(get_db)):
    payload = decode_token(request.refresh_token)

    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    username = payload.get("sub")
    user = db.query(UserModel).filter(UserModel.username == username).first()

    # Check the refresh token matches what we stored at login time.
    # If it doesn't match (e.g. user logged out, or token was revoked), reject it.
    if not user or user.refresh_token != request.refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token not recognized")

    # Issue a brand new pair of tokens (this is called "token rotation" -
    # a security best practice so old refresh tokens can't be reused)
    new_access_token = create_access_token(data={"sub": user.username})
    new_refresh_token = create_refresh_token(data={"sub": user.username})

    user.refresh_token = new_refresh_token
    db.commit()

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.post("/logout")
def logout(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    # Clearing the stored refresh token means it can never be used again,
    # even if someone has a copy of it
    current_user.refresh_token = None
    db.commit()
    return {"message": "Logged out successfully"}
