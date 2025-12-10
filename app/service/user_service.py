import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session

from ..model.user import User
from ..schemas.user import UserCreate, UserUpdate
from .auth import get_password_hash, verify_password
from ..model.exercise import Exercise
from ..model.level import Level
from ..model.user_exercise import UserExercise
from ..utils.time import wib_now


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_all_users(db: Session) -> List[User]:
    return db.query(User).order_by(User.created_at.desc()).all()


def create_user(db: Session, payload: UserCreate) -> User:
    # bcrypt membatasi password hingga 72 byte
    if len(payload.password.encode("utf-8")) > 72:
        raise ValueError("Password must be 72 bytes or fewer")
    if get_user_by_email(db, payload.email):
        raise ValueError("Email already registered")
    if get_user_by_username(db, payload.username):
        raise ValueError("Username already taken")

    hashed = get_password_hash(payload.password)
    now = wib_now()
    user = User(
        id=uuid.uuid4(),
        username=payload.username,
        email=payload.email,
        password=hashed,
        exp=0,
        streak=0,
        created_at=now,
        updated_at=now,
    )
    db.add(user)
    db.flush()  # to get defaults
    # Initialize UserExercise records for all exercises
    exercises = db.query(Exercise).all()
    for ex in exercises:
        level_count = db.query(Level).filter(Level.exercise_id == ex.id).count()
        ue = UserExercise(
            id=uuid.uuid4(),
            user_id=user.id,
            exercise_id=ex.id,
            max_level=level_count,
            current_level=0,
        )
        db.add(ue)
    return user


def authenticate_user(db: Session, *, email: str, password: str) -> Optional[User]:
    # Validasi panjang password sebelum verifikasi
    if len(password.encode("utf-8")) > 72:
        return None
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def update_user(db: Session, user_id: str, payload: UserUpdate) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    if payload.username is not None:
        user.username = payload.username
    if payload.email is not None:
        user.email = payload.email
    if payload.password is not None and payload.password.strip():
        user.password = get_password_hash(payload.password)
    # Perbarui timestamp updated_at secara manual
    user.updated_at = wib_now()
    db.flush()
    return user


def delete_user(db: Session, user_id: str) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    db.delete(user)
    return True


def update_streak_on_me(db: Session, current_user: User) -> None:
    now = wib_now()
    # If updated_at is None, initialize
    if not current_user.updated_at:
        current_user.streak = 1
        current_user.updated_at = now
        db.flush()
        return

    last = current_user.updated_at
    last_date = datetime(last.year, last.month, last.day)
    today_date = datetime(now.year, now.month, now.day)
    delta_days = (today_date - last_date).days

    if delta_days == 1:
        current_user.streak = int(current_user.streak or 0) + 1
        current_user.updated_at = now
        db.flush()
    elif delta_days > 1:
        current_user.streak = 1
        current_user.updated_at = now
        db.flush()
    else:
        # same day; no change
        pass