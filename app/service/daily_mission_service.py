from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..model.daily_mission import DailyMission
from ..model.user_level import UserLevel


def _wib_now() -> datetime:
    return datetime.utcnow() + timedelta(hours=7)


def _wib_day_range(now_wib: datetime):
    start_wib = datetime(now_wib.year, now_wib.month, now_wib.day)
    end_wib = start_wib + timedelta(days=1)
    # Convert WIB range to UTC-naive range for DB filtering (UTC+7)
    start_utc = start_wib - timedelta(hours=7)
    end_utc = end_wib - timedelta(hours=7)
    return start_utc, end_utc


def get_all_daily_missions(db: Session) -> List[DailyMission]:
    now_wib = _wib_now()
    start_utc, end_utc = _wib_day_range(now_wib)

    missions = db.query(DailyMission).all()

    # Precompute today stats from user_level
    today_user_levels = (
        db.query(UserLevel)
        .filter(UserLevel.created_at >= start_utc, UserLevel.created_at < end_utc)
        .all()
    )
    today_count = len(today_user_levels)
    today_star_sum = sum(ul.star or 0 for ul in today_user_levels)
    max_accuration = db.query(func.max(UserLevel.accuration)).scalar() or 0

    for m in missions:
        # Only process if not completed and updated_at is not today in WIB
        last_wib = (m.updated_at + timedelta(hours=7)) if m.updated_at else None
        if not m.is_completed and (last_wib is None or last_wib.date() != now_wib.date()):
            if m.type.lower() == 'exercise':
                m.current_progress = today_count
            elif m.type.lower() == 'star':
                m.current_progress = today_star_sum
            elif m.type.lower() == 'accuration':
                m.current_progress = max_accuration

            if m.current_progress >= m.max_progress:
                m.is_completed = True

            # Set updated_at to WIB time (stored naive)
            m.updated_at = now_wib

    db.flush()
    return missions