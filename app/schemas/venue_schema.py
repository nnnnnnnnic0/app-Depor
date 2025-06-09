# app/schemas/venue_schema.py

from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class VenueCreate(BaseModel):
    name: constr(min_length=3, max_length=100)
    address: Optional[constr(max_length=200)] = None
    city: Optional[constr(max_length=100)] = None
    capacity: Optional[int] = None

class VenueRead(VenueCreate):
    id: int
    created_at: datetime
    is_active: bool

class VenueUpdate(BaseModel):
    name: Optional[constr(min_length=3, max_length=100)] = None
    address: Optional[constr(max_length=200)] = None
    city: Optional[constr(max_length=100)] = None
    capacity: Optional[int] = None
    is_active: Optional[bool] = None
