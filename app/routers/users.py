# app/routers/users.py

from fastapi import APIRouter, Depends
from app.schemas.user_schema import UserRead
from app.routers.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get(
    "/me",
    response_model=UserRead,
    status_code=200
)
def read_users_me(
    current_user: User = Depends(get_current_user)
):
    """
    Devuelve los datos del usuario actualmente autenticado.
    """
    return current_user
