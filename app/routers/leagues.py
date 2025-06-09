# app/routers/leagues.py

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlmodel import Session, select
from app.database import get_session
from app.models.league import League
from app.schemas.league_schema import LeagueCreate, LeagueRead, LeagueUpdate
from app.routers.auth import get_current_active_superuser
from app.models.user import User


router = APIRouter(prefix="/leagues", tags=["Leagues"])

@router.post(
    "/",
    response_model=LeagueRead,
    status_code=status.HTTP_201_CREATED
)
def create_league(
    league_in: LeagueCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    league = League.from_orm(league_in)
    session.add(league)
    session.commit()
    session.refresh(league)
    return league

@router.get(
    "/",
    response_model=List[LeagueRead],
    status_code=status.HTTP_200_OK
)
def list_leagues(session: Session = Depends(get_session)):
    leagues = session.exec(select(League)).all()
    return leagues

@router.get(
    "/{league_id}",
    response_model=LeagueRead,
    status_code=status.HTTP_200_OK
)
def get_league(
    league_id: int,
    session: Session = Depends(get_session)
):
    league = session.get(League, league_id)
    if not league:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="League not found"
        )
    return league

@router.put(
    "/{league_id}",
    response_model=LeagueRead,
    status_code=status.HTTP_200_OK
)
def update_league(
    league_id: int,
    league_in: LeagueUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    league = session.get(League, league_id)
    if not league:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="League not found"
        )
    league_data = league_in.dict(exclude_unset=True)
    for key, value in league_data.items():
        setattr(league, key, value)
    session.add(league)
    session.commit()
    session.refresh(league)
    return league

@router.delete(
    "/{league_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_league(
    league_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    league = session.get(League, league_id)
    if not league:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="League not found"
        )
    # Soft-delete: marcar como inactiva
    league.is_active = False
    session.add(league)
    session.commit()
    return None