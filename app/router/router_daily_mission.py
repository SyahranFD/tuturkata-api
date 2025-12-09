from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..config.database import get_db
from ..schemas.daily_mission import DailyMissionOut
from ..service.daily_mission_service import get_all_daily_missions
from ..service.auth import get_current_user
from ..model.user import User


router_daily_mission = APIRouter(prefix="/api/daily-missions", tags=["Daily Missions"])


@router_daily_mission.get("/", response_model=List[DailyMissionOut])
def list_daily_missions(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return get_all_daily_missions(db)