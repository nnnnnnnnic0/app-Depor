# app/routers/teams.py

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlmodel import Session, select
from app.database import get_session
from app.models.team import Team
from app.schemas.team_schema import TeamCreate, TeamRead, TeamUpdate
from app.routers.auth import get_current_active_superuser
from app.models.user import User

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.post(
    "/",
    response_model=TeamRead,
    status_code=status.HTTP_201_CREATED
)
def create_team(
    team_in: TeamCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    team = Team.from_orm(team_in)
    session.add(team)
    session.commit()
    session.refresh(team)
    return team

@router.get(
    "/",
    response_model=List[TeamRead],
    status_code=status.HTTP_200_OK
)
def list_teams(session: Session = Depends(get_session)):
    teams = session.exec(select(Team)).all()
    return teams

@router.get(
    "/{team_id}",
    response_model=TeamRead,
    status_code=status.HTTP_200_OK
)
def get_team(
    team_id: int,
    session: Session = Depends(get_session)
):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    return team

@router.put(
    "/{team_id}",
    response_model=TeamRead,
    status_code=status.HTTP_200_OK
)
def update_team(
    team_id: int,
    team_in: TeamUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    team_data = team_in.dict(exclude_unset=True)
    for key, value in team_data.items():
        setattr(team, key, value)
    session.add(team)
    session.commit()
    session.refresh(team)
    return team

@router.delete(
    "/{team_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_team(
    team_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    # Hard delete: eliminar el registro
    session.delete(team)
    session.commit()
    return None
