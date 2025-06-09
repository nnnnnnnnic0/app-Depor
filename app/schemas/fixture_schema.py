# app/schemas/fixture_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FixtureCreate(BaseModel):
    league_id: int
    home_team_id: int
    away_team_id: int
    venue_id: int
    match_datetime: datetime

class FixtureRead(FixtureCreate):
    id: int
    is_active: bool
    created_at: datetime

class FixtureUpdate(BaseModel):
    league_id: Optional[int] = None
    home_team_id: Optional[int] = None
    away_team_id: Optional[int] = None
    venue_id: Optional[int] = None
    match_datetime: Optional[datetime] = None
    is_active: Optional[bool] = None
