import uuid
from typing import Optional, List
from sqlalchemy.orm import Session

from ..model.level_quiz import LevelQuiz
from ..schemas.level_quiz import LevelQuizCreate, LevelQuizUpdate


def get_level_quiz_by_id(db: Session, level_quiz_id: str) -> Optional[LevelQuiz]:
    return db.query(LevelQuiz).filter(LevelQuiz.id == level_quiz_id).first()


def get_all_level_quizzes(db: Session) -> List[LevelQuiz]:
    return db.query(LevelQuiz).all()


def create_level_quiz(db: Session, payload: LevelQuizCreate) -> LevelQuiz:
    level_quiz = LevelQuiz(
        id=uuid.uuid4(),
        level_id=payload.level_id,
        instruction=payload.instruction,
        question=payload.question,
    )
    db.add(level_quiz)
    db.flush()
    return level_quiz


def update_level_quiz(db: Session, level_quiz_id: str, payload: LevelQuizUpdate) -> Optional[LevelQuiz]:
    level_quiz = get_level_quiz_by_id(db, level_quiz_id)
    if not level_quiz:
        return None
    if payload.level_id is not None:
        level_quiz.level_id = payload.level_id
    if payload.instruction is not None:
        level_quiz.instruction = payload.instruction
    if payload.question is not None:
        level_quiz.question = payload.question
    db.flush()
    return level_quiz


def delete_level_quiz(db: Session, level_quiz_id: str) -> bool:
    level_quiz = get_level_quiz_by_id(db, level_quiz_id)
    if not level_quiz:
        return False
    db.delete(level_quiz)
    return True