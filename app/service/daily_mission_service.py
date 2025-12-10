from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..model.daily_mission import DailyMission
from ..model.user_level import UserLevel
from ..utils.time import wib_now


def get_all_daily_missions(db: Session) -> List[DailyMission]:
    now_wib = wib_now()
    # Gunakan rentang hari WIB (tanpa konversi ke UTC)
    start_wib = datetime(now_wib.year, now_wib.month, now_wib.day)
    end_wib = start_wib + timedelta(days=1)

    missions = db.query(DailyMission).all()

    # Precompute today stats from user_level
    today_user_levels = (
        db.query(UserLevel)
        .filter(UserLevel.updated_at >= start_wib, UserLevel.updated_at < end_wib)
        .all()
    )
    today_count = len(today_user_levels)
    today_star_sum = sum(ul.star or 0 for ul in today_user_levels)
    max_accuration = max((ul.accuration or 0) for ul in today_user_levels) if today_user_levels else 0
    
    for mission in missions:
        # Selalu hitung ulang progress pada setiap request
        mission_type = mission.type.lower() if mission.type else ""
        if mission_type == 'exercise':
            mission.current_progress = today_count
        elif mission_type == 'star':
            mission.current_progress = today_star_sum
        elif mission_type == 'accuration':
            mission.current_progress = max_accuration
        else:
            mission.current_progress = 0

        # Tetapkan status completed berdasarkan progress saat ini
        mission.is_completed = mission.current_progress >= mission.max_progress

        # Set updated_at ke waktu WIB (naive) setiap kali endpoint dipanggil
        mission.updated_at = now_wib

    db.flush()
    return missions