from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from ..config.database import get_db
from ..schemas.user import UserCreate, UserOut, UserUpdate, TokenOut, UserLogin
from ..service.user_service import *
from ..service.auth import create_access_token, get_current_user
from ..model.user import User


router_user = APIRouter(prefix="/api/users", tags=["Users"])


@router_user.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(db, payload)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router_user.post("/login", response_model=TokenOut)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, email=payload.email, password=payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(subject=str(user.id))
    return TokenOut(access_token=access_token)


@router_user.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

@router_user.put("/{user_id}", response_model=UserOut)
def update_user_endpoint(user_id: str, payload: UserUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    user = update_user(db, user_id, payload)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
