from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.rate_limit import limiter
from app.routes import colaboradores, planos, cardapios, refeicoes, chat, alertas
from app.routes import auth as auth_routes
from app.database import init_db
from app.config import get_settings
from app.logging_config import setup_logging
import logging
import time
import uuid

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="NutriOffshore AI",
    description="Agente Nutricionista Virtual para Ambientes Offshore",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

_settings = get_settings()
_cors_origins = [
    origin.strip()
    for origin in _settings.CORS_ORIGINS.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    start_time = time.time()

    # Skip noisy health checks
    if request.url.path == "/health":
        return await call_next(request)

    logger.info(
        "Request started",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host if request.client else "unknown",
        },
    )

    try:
        response = await call_next(request)
        duration_ms = round((time.time() - start_time) * 1000)

        log_level = logging.WARNING if response.status_code >= 400 else logging.INFO
        logger.log(
            log_level,
            "Request completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        )
        response.headers["X-Request-ID"] = request_id
        return response
    except Exception as e:
        duration_ms = round((time.time() - start_time) * 1000)
        logger.error(
            "Request failed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "duration_ms": duration_ms,
                "error_detail": str(e),
            },
            exc_info=True,
        )
        raise


app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["Autenticacao"])
app.include_router(colaboradores.router, prefix="/api/v1/colaboradores", tags=["Colaboradores"])
app.include_router(planos.router, prefix="/api/v1/planos", tags=["Planos Nutricionais"])
app.include_router(cardapios.router, prefix="/api/v1/cardapios", tags=["Cardápios"])
app.include_router(refeicoes.router, prefix="/api/v1/refeicoes", tags=["Refeições"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat AI"])
app.include_router(alertas.router, prefix="/api/v1/alertas", tags=["Alertas Médicos"])


@app.api_route("/health", methods=["GET", "HEAD", "POST", "OPTIONS"])
async def health_check():
    return {"status": "healthy", "service": "NutriOffshore AI"}


@app.on_event("startup")
async def startup():
    _settings.validate_settings()
    await init_db()
    logger.info("NutriOffshore AI Backend started successfully")
