from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import colaboradores, planos, cardapios, refeicoes, chat, alertas
from app.database import init_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="NutriOffshore AI",
    description="Agente Nutricionista Virtual para Ambientes Offshore",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(colaboradores.router, prefix="/api/v1/colaboradores", tags=["Colaboradores"])
app.include_router(planos.router, prefix="/api/v1/planos", tags=["Planos Nutricionais"])
app.include_router(cardapios.router, prefix="/api/v1/cardapios", tags=["Cardapios"])
app.include_router(refeicoes.router, prefix="/api/v1/refeicoes", tags=["Refeicoes"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat AI"])
app.include_router(alertas.router, prefix="/api/v1/alertas", tags=["Alertas Medicos"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "NutriOffshore AI"}

@app.on_event("startup")
async def startup():
    await init_db()
    logger.info("NutriOffshore AI Backend started successfully")
