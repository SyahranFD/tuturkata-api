import uuid
from datetime import datetime
from sqlalchemy.orm import Session

from app.model.user import User
from app.service.auth import get_password_hash


def seed_users(db: Session) -> None:
    samples = [
        {
            "username": "admin",
            "email": "admin@gmail.com",
            "password": "admin",
        },
    ]

    for s in samples:
        exists = db.query(User).filter(User.email == s["email"]).first()
        if exists:
            continue
        now = datetime.utcnow()
        user = User(
            id=uuid.uuid4(),
            username=s["username"],
            email=s["email"],
            password=get_password_hash(s["password"]),
            created_at=now,
            updated_at=now,
        )
        db.add(user)


if __name__ == "__main__":
    # Jalankan langsung untuk seed user saja
    from app.config.database import SessionLocal

    db = SessionLocal()
    try:
        seed_users(db)
        db.commit()
        print("Seed users selesai.")
    except Exception as e:
        db.rollback()
        print(f"Seed users gagal: {e}")
        raise
    finally:
        db.close()