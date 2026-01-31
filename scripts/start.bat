@echo off
echo ============================================
echo    NutriOffshore AI - Iniciando...
echo ============================================
echo.

cd /d "%~dp0.."

if not exist .env (
    echo [ERRO] Arquivo .env nao encontrado!
    echo Copie .env.example para .env e configure sua ANTHROPIC_API_KEY
    echo.
    echo   copy .env.example .env
    echo   notepad .env
    echo.
    pause
    exit /b 1
)

echo Verificando Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Docker nao encontrado! Instale o Docker Desktop.
    echo https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

echo Docker encontrado. Iniciando containers...
echo.
docker-compose up --build

pause
