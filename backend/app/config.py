from pydantic_settings import BaseSettings
from functools import lru_cache

_INSECURE_DEFAULT_SECRET = "nutrioffshore-secret-key-change-in-production"

class Settings(BaseSettings):
    APP_NAME: str = "NutriOffshore AI"
    DEBUG: bool = False
    DATABASE_URL: str = ""
    DATABASE_URL_SYNC: str = "postgresql://postgres:postgres@db:5432/nutrioffshore"
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "google/gemma-3-27b-it:free"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    AUTH_ENABLED: bool = False
    JWT_SECRET: str = ""
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    CORS_ORIGINS: str = "http://localhost:3000"

    class Config:
        env_file = ".env"

    def validate_settings(self) -> None:
        """Valida configuracoes criticas na inicializacao.
        Levanta ValueError se segredos nao estiverem definidos corretamente.
        """
        if self.AUTH_ENABLED:
            if not self.JWT_SECRET or self.JWT_SECRET == _INSECURE_DEFAULT_SECRET:
                raise ValueError(
                    "JWT_SECRET nao configurado. Defina um segredo forte na variavel de ambiente JWT_SECRET."
                )
        if not self.DATABASE_URL:
            raise ValueError(
                "DATABASE_URL nao configurado. Defina a URL do banco na variavel de ambiente DATABASE_URL."
            )

@lru_cache()
def get_settings():
    return Settings()
