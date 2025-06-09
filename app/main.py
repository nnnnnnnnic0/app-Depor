# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# Importamos el router de leagues
from app.routers.leagues import router as leagues_router
from app.routers.teams import router as teams_router
from app.routers.players import router as players_router
from app.routers.venues import router as venues_router
from app.routers.fixtures import router as fixtures_router
from app.routers.payments import router as payments_router
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router







app = FastAPI(
    title="Sports Platform API",
    description="API para gestión de ligas, equipos, jugadores, pagos, etc.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluimos el router en FastAPI
app.include_router(leagues_router)
app.include_router(teams_router)
app.include_router(players_router)
app.include_router(venues_router)
app.include_router(fixtures_router)
app.include_router(payments_router)
app.include_router(auth_router)
app.include_router(users_router)







@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
