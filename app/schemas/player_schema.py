# app/schemas/player_schema.py

from pydantic import BaseModel, constr
from typing import Optional
from datetime import date, datetime

class PlayerCreate(BaseModel):
    first_name: constr(min_length=1, max_length=50)
    last_name: constr(min_length=1, max_length=50)
    birthdate: Optional[date] = None
    position: Optional[constr(max_length=50)] = None
    jersey_number: Optional[int] = None
    team_id: int

class PlayerRead(PlayerCreate):
    id: int
    created_at: datetime
    is_active: bool

class PlayerUpdate(BaseModel):
    first_name: Optional[constr(min_length=1, max_length=50)] = None
    last_name: Optional[constr(min_length=1, max_length=50)] = None
    birthdate: Optional[date] = None
    position: Optional[constr(max_length=50)] = None
    jersey_number: Optional[int] = None
    team_id: Optional[int] = None
    is_active: Optional[bool] = None
