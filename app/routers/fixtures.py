# app/routers/fixtures.py

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlmodel import Session, select
from app.database import get_session
from app.models.fixture import Fixture
from app.schemas.fixture_schema import FixtureCreate, FixtureRead, FixtureUpdate
from app.routers.auth import get_current_active_superuser
from app.models.user import User


router = APIRouter(prefix="/fixtures", tags=["Fixtures"])

@router.post(
    "/",
    response_model=FixtureRead,
    status_code=status.HTTP_201_CREATED
)
def create_fixture(
    fixture_in: FixtureCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    fixture = Fixture.from_orm(fixture_in)
    session.add(fixture)
    session.commit()
    session.refresh(fixture)
    return fixture

@router.get(
    "/",
    response_model=List[FixtureRead],
    status_code=status.HTTP_200_OK
)
def list_fixtures(session: Session = Depends(get_session)):
    fixtures = session.exec(select(Fixture)).all()
    return fixtures

@router.get(
    "/{fixture_id}",
    response_model=FixtureRead,
    status_code=status.HTTP_200_OK
)
def get_fixture(
    fixture_id: int,
    session: Session = Depends(get_session)
):
    fixture = session.get(Fixture, fixture_id)
    if not fixture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fixture not found"
        )
    return fixture

@router.put(
    "/{fixture_id}",
    response_model=FixtureRead,
    status_code=status.HTTP_200_OK
)
def update_fixture(
    fixture_id: int,
    fixture_in: FixtureUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    fixture = session.get(Fixture, fixture_id)
    if not fixture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fixture not found"
        )
    fixture_data = fixture_in.dict(exclude_unset=True)
    for key, value in fixture_data.items():
        setattr(fixture, key, value)
    session.add(fixture)
    session.commit()
    session.refresh(fixture)
    return fixture

@router.delete(
    "/{fixture_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_fixture(
    fixture_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    fixture = session.get(Fixture, fixture_id)
    if not fixture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fixture not found"
        )
    # Soft-delete: marcar como inactivo
    fixture.is_active = False
    session.add(fixture)
    session.commit()
    return None
