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
    return db.query(LevelQuiz).all()


def get_level_quizzes_by_level_id(db: Session, level_id: str) -> List[LevelQuiz]:
    level = db.query(Level).filter(Level.id == level_id).first()
    if not level:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")
    return db.query(LevelQuiz).filter(LevelQuiz.level_id == level_id).all()


def create_level_quiz(db: Session, payload: LevelQuizCreate) -> LevelQuiz:
    # Validasi parent level
    level = db.query(Level).filter(Level.id == payload.level_id).first()
    if not level:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")
    # Validasi input
    if not payload.instruction or not payload.instruction.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Instruction is required")
    if not payload.question or not payload.question.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Question is required")

    level_quiz = LevelQuiz(
        id=uuid.uuid4(),
        level_id=payload.level_id,
        instruction=payload.instruction.strip(),
        question=payload.question.strip(),
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
    if payload.question is not None:
        if not payload.question.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Question cannot be empty")
        level_quiz.question = payload.question.strip()
    db.flush()
    return level_quiz


def delete_level_quiz(db: Session, level_quiz_id: str) -> bool:
    level_quiz = get_level_quiz_by_id(db, level_quiz_id)
    if not level_quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level Quiz not found")
    db.delete(level_quiz)
    return True