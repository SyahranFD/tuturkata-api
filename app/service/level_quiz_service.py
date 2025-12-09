import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..model.level_quiz import LevelQuiz
from ..model.level import Level
from ..schemas.level_quiz import LevelQuizCreate, LevelQuizUpdate


def get_level_quiz_by_id(db: Session, level_quiz_id: str) -> Optional[LevelQuiz]:
    return db.query(LevelQuiz).filter(LevelQuiz.id == level_quiz_id).first()


def get_all_level_quizzes(db: Session) -> List[LevelQuiz]:
    return db.query(LevelQuiz).order_by(LevelQuiz.order.asc()).all()


def get_level_quizzes_by_level_id(db: Session, level_id: str) -> List[LevelQuiz]:
    level = db.query(Level).filter(Level.id == level_id).first()
    if not level:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")
    return (
        db.query(LevelQuiz)
        .filter(LevelQuiz.level_id == level_id)
        .order_by(LevelQuiz.order.asc())
        .all()
    )


def create_level_quiz(db: Session, payload: LevelQuizCreate) -> LevelQuiz:
    # Validasi parent level
    level = db.query(Level).filter(Level.id == payload.level_id).first()
    if not level:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")
    # Validasi input
    if payload.order is None or payload.order < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order must be >= 0")
    if not payload.instruction or not payload.instruction.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Instruction is required")
    if not payload.speech_text or not payload.speech_text.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Speech text is required")

    level_quiz = LevelQuiz(
        id=uuid.uuid4(),
        level_id=payload.level_id,
        order=payload.order,
        instruction=payload.instruction.strip(),
        speech_text=payload.speech_text.strip(),
        exp=payload.exp,
    )
    db.add(level_quiz)
    db.flush()
    return level_quiz


def update_level_quiz(db: Session, level_quiz_id: str, payload: LevelQuizUpdate) -> Optional[LevelQuiz]:
    level_quiz = get_level_quiz_by_id(db, level_quiz_id)
    if not level_quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level Quiz not found")
    if payload.level_id is not None:
        level = db.query(Level).filter(Level.id == payload.level_id).first()
        if not level:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")
        level_quiz.level_id = payload.level_id
    if payload.instruction is not None:
        if not payload.instruction.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Instruction cannot be empty")
        level_quiz.instruction = payload.instruction.strip()
    if payload.speech_text is not None:
        if not payload.speech_text.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Speech text cannot be empty")
        level_quiz.speech_text = payload.speech_text.strip()
    if payload.order is not None:
        if payload.order < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order must be >= 0")
        level_quiz.order = payload.order
    if payload.exp is not None:
        if payload.exp < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Exp must be >= 0")
        level_quiz.exp = payload.exp
    db.flush()
    return level_quiz


def delete_level_quiz(db: Session, level_quiz_id: str) -> bool:
    level_quiz = get_level_quiz_by_id(db, level_quiz_id)
    if not level_quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level Quiz not found")
    db.delete(level_quiz)
    return True