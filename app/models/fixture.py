# app/models/fixture.py

from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Fixture(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    league_id: int = Field(foreign_key="league.id")
    home_team_id: int = Field(foreign_key="team.id")
    away_team_id: int = Field(foreign_key="team.id")
    venue_id: int = Field(foreign_key="venue.id")
    match_datetime: datetime = Field(nullable=False, index=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
