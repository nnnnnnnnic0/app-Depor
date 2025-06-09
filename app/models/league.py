# app/models/league.py

from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field

class League(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    season_start: date
    season_end: date
    budget: float
    description: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
