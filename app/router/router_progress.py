from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..config.database import get_db
from ..service.progress_service import (
    get_summary_progress,
    get_summary_progress_weekly,
    get_chart_activity_weekly,
)
from ..service.auth import get_current_user
from ..model.user import User
from ..schemas.progress import SummaryProgressOut, ChartActivityWeeklyOut


router_progress = APIRouter(prefix="/api/progress", tags=["Progress"])


@router_progress.get("/summary", response_model=SummaryProgressOut)
def summary_progress(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_summary_progress(db, str(current_user.id))


@router_progress.get("/summary-weekly", response_model=SummaryProgressOut)
def summary_progress_weekly(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_summary_progress_weekly(db, str(current_user.id))


@router_progress.get("/chart-activity-weekly", response_model=ChartActivityWeeklyOut)
def chart_activity_weekly(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_chart_activity_weekly(db, str(current_user.id))