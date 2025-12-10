from datetime import datetime, timedelta
from typing import Dict, List

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..model.user import User
from ..model.user_level import UserLevel
from ..utils.time import wib_now


def get_summary_progress(db: Session, user_id: str) -> Dict:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")

    streak = int(user.streak or 0)
    exp = int(user.exp or 0)
    acc_avg = db.query(func.avg(UserLevel.accuration)).filter(UserLevel.user_id == user_id).scalar()
    exercise_total = db.query(func.count(UserLevel.id)).filter(UserLevel.user_id == user_id).scalar() or 0

    return {
        "streak": streak,
        "exp": exp,
        "accuration": int(round(acc_avg or 0)),
        "exercise_total": int(exercise_total),
    }


def get_summary_progress_weekly(db: Session, user_id: str) -> Dict:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")

    now = wib_now()
    # Start of week (Monday) in WIB
    today_start = datetime(now.year, now.month, now.day)
    start_of_week = today_start - timedelta(days=now.weekday())
    end_of_week = start_of_week + timedelta(days=7)

    # Weekly stats based on UserLevel.updated_at within WIB range
    acc_avg = (
        db.query(func.avg(UserLevel.accuration))
        .filter(
            UserLevel.user_id == user_id,
            UserLevel.updated_at >= start_of_week,
            UserLevel.updated_at < end_of_week,
        )
        .scalar()
    )
    exercise_total = (
        db.query(func.count(UserLevel.id))
        .filter(
            UserLevel.user_id == user_id,
            UserLevel.updated_at >= start_of_week,
            UserLevel.updated_at < end_of_week,
        )
        .scalar()
        or 0
    )

    # Keep exp and streak from user table (cumulative), as weekly exp history is not stored
    streak = int(user.streak or 0)
    exp = int(user.exp or 0)

    return {
        "streak": streak,
        "exp": exp,
        "accuration": int(round(acc_avg or 0)),
        "exercise_total": int(exercise_total),
    }


def get_chart_activity_weekly(db: Session, user_id: str) -> Dict:
    now = wib_now()
    today_start = datetime(now.year, now.month, now.day)
    start_of_week = today_start - timedelta(days=now.weekday())
    end_of_week = start_of_week + timedelta(days=7)

    rows: List[UserLevel] = (
        db.query(UserLevel)
        .filter(
            UserLevel.user_id == user_id,
            UserLevel.updated_at >= start_of_week,
            UserLevel.updated_at < end_of_week,
        )
        .all()
    )

    labels = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]
    counts = [0] * 7

    for ul in rows:
        if not ul.updated_at:
            continue
        # Map Python weekday (Mon=0..Sun=6) directly
        idx = ul.updated_at.weekday()
        if 0 <= idx < 7:
            counts[idx] += 1

    return {"labels": labels, "counts": counts}