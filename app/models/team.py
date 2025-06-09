# app/models/team.py

from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    logo_url: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    league_id: int = Field(foreign_key="league.id")

    # Si más adelante quieres acceder a la liga desde el equipo:
    # league: Optional["League"] = Relationship(back_populates="teams")
