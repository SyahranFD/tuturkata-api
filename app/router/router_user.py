from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from ..config.database import get_db
from ..schemas.user import UserCreate, UserOut, UserUpdate, TokenOut, UserLogin
from ..service.user_service import (
    create_user,
    authenticate_user,
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user,
)
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
    # Login hanya menerima email dan password (JSON body)
    if len(payload.password.encode("utf-8")) > 72:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be 72 bytes or fewer")
    user = authenticate_user(db, email=payload.email, password=payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(subject=str(user.id))
    return TokenOut(access_token=access_token)


@router_user.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@router_user.get("/", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return get_all_users(db)


@router_user.get("/{user_id}", response_model=UserOut)
def read_user(user_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router_user.put("/{user_id}", response_model=UserOut)
def update_user_endpoint(user_id: str, payload: UserUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    user = update_user(db, user_id, payload)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router_user.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    deleted = delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return None