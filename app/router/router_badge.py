from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..config.database import get_db
from ..schemas.badge import BadgeOut
from ..service.badge_service import get_badges_by_user_id
from ..service.auth import get_current_user
from ..model.user import User


router_badge = APIRouter(prefix="/api/badges", tags=["Badges"])


@router_badge.get("/", response_model=List[BadgeOut])
def list_my_badges(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_badges_by_user_id(db, str(current_user.id))