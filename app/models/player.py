# app/models/player.py

from typing import Optional
from datetime import date, datetime
from sqlmodel import SQLModel, Field, Relationship

class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(nullable=False, index=True)
    last_name: str = Field(nullable=False, index=True)
    birthdate: Optional[date] = Field(default=None)
    position: Optional[str] = Field(default=None, max_length=50)
    jersey_number: Optional[int] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    team_id: int = Field(foreign_key="team.id")

    # Si en el futuro quieres navegar de Player → Team:
    # team: Optional["Team"] = Relationship(back_populates="players")
