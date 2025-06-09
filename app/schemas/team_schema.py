# app/schemas/team_schema.py

from pydantic import BaseModel, constr, HttpUrl
from typing import Optional
from datetime import datetime

class TeamCreate(BaseModel):
    name: constr(min_length=3, max_length=100)
    logo_url: Optional[HttpUrl] = None
    league_id: int

class TeamRead(TeamCreate):
    id: int
    created_at: datetime

class TeamUpdate(BaseModel):
    name: Optional[constr(min_length=3, max_length=100)] = None
    logo_url: Optional[HttpUrl] = None
    league_id: Optional[int] = None
