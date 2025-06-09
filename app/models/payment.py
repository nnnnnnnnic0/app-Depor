# app/models/payment.py

from typing import Optional
from datetime import date, datetime
from sqlmodel import SQLModel, Field

class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    player_id: int = Field(foreign_key="player.id")
    amount: float = Field(nullable=False)
    payment_date: date = Field(nullable=False, index=True)
    method: Optional[str] = Field(default=None, max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
