# app/config.py

import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de .env

class Settings:
    APP_PORT: int = int(os.getenv("PORT", 8000))
    TZ: str = os.getenv("TZ", "UTC")

    # Usamos única VARIABLE DATABASE_URL
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./dev.db"  # valor por defecto si no existe en .env
    )

    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

    # Stripe
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")

settings = Settings()

# (Opcional) Verificación rápida – puedes comentarlo después de confirmar:
print(f"[Config] DATABASE_URL={settings.DATABASE_URL}, TZ={settings.TZ}")
