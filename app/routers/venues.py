# app/routers/venues.py

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlmodel import Session, select
from app.database import get_session
from app.models.venue import Venue
from app.schemas.venue_schema import VenueCreate, VenueRead, VenueUpdate
from app.routers.auth import get_current_active_superuser
from app.models.user import User


router = APIRouter(prefix="/venues", tags=["Venues"])

@router.post(
    "/",
    response_model=VenueRead,
    status_code=status.HTTP_201_CREATED
)
def create_venue(
    venue_in: VenueCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    venue = Venue.from_orm(venue_in)
    session.add(venue)
    session.commit()
    session.refresh(venue)
    return venue

@router.get(
    "/",
    response_model=List[VenueRead],
    status_code=status.HTTP_200_OK
)
def list_venues(session: Session = Depends(get_session)):
    venues = session.exec(select(Venue)).all()
    return venues

@router.get(
    "/{venue_id}",
    response_model=VenueRead,
    status_code=status.HTTP_200_OK
)
def get_venue(
    venue_id: int,
    session: Session = Depends(get_session)
):
    venue = session.get(Venue, venue_id)
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )
    return venue

@router.put(
    "/{venue_id}",
    response_model=VenueRead,
    status_code=status.HTTP_200_OK
)
def update_venue(
    venue_id: int,
    venue_in: VenueUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    venue = session.get(Venue, venue_id)
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )
    venue_data = venue_in.dict(exclude_unset=True)
    for key, value in venue_data.items():
        setattr(venue, key, value)
    session.add(venue)
    session.commit()
    session.refresh(venue)
    return venue

@router.delete(
    "/{venue_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_venue(
    venue_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    venue = session.get(Venue, venue_id)
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )
    # Soft-delete: marcar como inactivo
    venue.is_active = False
    session.add(venue)
    session.commit()
    return None
