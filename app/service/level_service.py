import uuid
from typing import Optional, List
from sqlalchemy.orm import Session

from ..model.level import Level
from ..schemas.level import LevelCreate, LevelUpdate


def get_level_by_id(db: Session, level_id: str) -> Optional[Level]:
    return db.query(Level).filter(Level.id == level_id).first()


def get_all_levels(db: Session) -> List[Level]:
    return db.query(Level).order_by(Level.order.asc()).all()


def create_level(db: Session, payload: LevelCreate) -> Level:
    level = Level(
        id=uuid.uuid4(),
        exercise_id=payload.exercise_id,
        order=payload.order,
        title=payload.title,
        desc=payload.desc,
    )
    db.add(level)
    db.flush()
    return level


def update_level(db: Session, level_id: str, payload: LevelUpdate) -> Optional[Level]:
    level = get_level_by_id(db, level_id)
    if not level:
        return None
    if payload.exercise_id is not None:
        level.exercise_id = payload.exercise_id
    if payload.order is not None:
        level.order = payload.order
    if payload.title is not None:
        level.title = payload.title
    if payload.desc is not None:
        level.desc = payload.desc
    db.flush()
    return level


def delete_level(db: Session, level_id: str) -> bool:
    level = get_level_by_id(db, level_id)
    if not level:
        return False
    db.delete(level)
    return True