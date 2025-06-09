# app/schemas/payment_schema.py

from pydantic import BaseModel, confloat, constr
from typing import Optional
from datetime import date, datetime

class PaymentCreate(BaseModel):
    player_id: int
    amount: confloat(gt=0)
    payment_date: date
    method: Optional[constr(max_length=50)] = None

class PaymentRead(PaymentCreate):
    id: int
    created_at: datetime
    is_active: bool

class PaymentUpdate(BaseModel):
    player_id: Optional[int] = None
    amount: Optional[confloat(gt=0)] = None
    payment_date: Optional[date] = None
    method: Optional[constr(max_length=50)] = None
    is_active: Optional[bool] = None
