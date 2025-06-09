# app/schemas/league_schema.py

from pydantic import BaseModel, constr
from datetime import date
from typing import Optional

class LeagueCreate(BaseModel):
    name: constr(min_length=3, max_length=100)
    season_start: date
    season_end: date
    budget: float
    description: Optional[str] = None

class LeagueRead(LeagueCreate):
    id: int
    is_active: bool

class LeagueUpdate(BaseModel):
    name: Optional[constr(min_length=3, max_length=100)] = None
    season_start: Optional[date] = None
    season_end: Optional[date] = None
    budget: Optional[float] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
