from typing import List
from pydantic import BaseModel


class SummaryProgressOut(BaseModel):
    streak: int
    exp: int
    accuration: int
    exercise_total: int


class ChartActivityWeeklyOut(BaseModel):
    labels: List[str]
    counts: List[int]