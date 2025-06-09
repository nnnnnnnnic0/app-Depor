# app/routers/players.py

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlmodel import Session, select
from app.database import get_session
from app.models.player import Player
from app.schemas.player_schema import PlayerCreate, PlayerRead, PlayerUpdate
from app.routers.auth import get_current_active_superuser
from app.models.user import User


router = APIRouter(prefix="/players", tags=["Players"])

@router.post(
    "/",
    response_model=PlayerRead,
    status_code=status.HTTP_201_CREATED
)
def create_player(
    player_in: PlayerCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    player = Player.from_orm(player_in)
    session.add(player)
    session.commit()
    session.refresh(player)
    return player

@router.get(
    "/",
    response_model=List[PlayerRead],
    status_code=status.HTTP_200_OK
)
def list_players(session: Session = Depends(get_session)):
    players = session.exec(select(Player)).all()
    return players

@router.get(
    "/{player_id}",
    response_model=PlayerRead,
    status_code=status.HTTP_200_OK
)
def get_player(
    player_id: int,
    session: Session = Depends(get_session)
):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    return player

@router.put(
    "/{player_id}",
    response_model=PlayerRead,
    status_code=status.HTTP_200_OK
)
def update_player(
    player_id: int,
    player_in: PlayerUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    player_data = player_in.dict(exclude_unset=True)
    for key, value in player_data.items():
        setattr(player, key, value)
    session.add(player)
    session.commit()
    session.refresh(player)
    return player

@router.delete(
    "/{player_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_player(
    player_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    # Soft-delete: marcamos como inactivo
    player.is_active = False
    session.add(player)
    session.commit()
    return None
