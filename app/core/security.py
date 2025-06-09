# app/core/security.py

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

# ------------------------
# 1. Contexto de encriptación
# ------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Recibe un password en texto claro y devuelve el hash usando bcrypt.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica que el password plano coincida con el hash bcrypt guardado.
    """
    return pwd_context.verify(plain_password, hashed_password)


# ------------------------
# 2. Funciones para JWT
# ------------------------

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT con la información en `data` y expira en `expires_delta` minutos 
    (o el valor por defecto de settings.ACCESS_TOKEN_EXPIRE_MINUTES).
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,     # ← actualizado
        algorithm=settings.JWT_ALGORITHM  # ← actualizado
    )
    return encoded_jwt


def verify_access_token(token: str) -> Optional[dict]:
    """
    Decodifica el token y devuelve el payload (claims) si es válido.
    Si no, retorna None.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
