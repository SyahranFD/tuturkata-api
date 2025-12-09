from typing import List
from sqlalchemy.orm import Session

from ..model.badge import Badge


def get_badges_by_user_id(db: Session, user_id: str) -> List[Badge]:
    return db.query(Badge).filter(Badge.user_id == user_id).all()