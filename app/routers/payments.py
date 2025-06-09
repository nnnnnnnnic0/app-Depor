# app/routers/payments.py

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlmodel import Session, select
from app.database import get_session
from app.models.payment import Payment
from app.schemas.payment_schema import PaymentCreate, PaymentRead, PaymentUpdate
from app.routers.auth import get_current_active_superuser
from app.models.user import User


router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post(
    "/",
    response_model=PaymentRead,
    status_code=status.HTTP_201_CREATED
)
def create_payment(
    payment_in: PaymentCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    payment = Payment.from_orm(payment_in)
    session.add(payment)
    session.commit()
    session.refresh(payment)
    return payment

@router.get(
    "/",
    response_model=List[PaymentRead],
    status_code=status.HTTP_200_OK
)
def list_payments(session: Session = Depends(get_session)):
    payments = session.exec(select(Payment)).all()
    return payments

@router.get(
    "/{payment_id}",
    response_model=PaymentRead,
    status_code=status.HTTP_200_OK
)
def get_payment(
    payment_id: int,
    session: Session = Depends(get_session)
):
    payment = session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return payment

@router.put(
    "/{payment_id}",
    response_model=PaymentRead,
    status_code=status.HTTP_200_OK
)
def update_payment(
    payment_id: int,
    payment_in: PaymentUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    payment = session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    payment_data = payment_in.dict(exclude_unset=True)
    for key, value in payment_data.items():
        setattr(payment, key, value)
    session.add(payment)
    session.commit()
    session.refresh(payment)
    return payment

@router.delete(
    "/{payment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_payment(
    payment_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    payment = session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    # Soft-delete: marcar como inactivo
    payment.is_active = False
    session.add(payment)
    session.commit()
    return None
