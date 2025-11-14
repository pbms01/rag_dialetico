@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM EXECUTAR APLICAÇÃO - SISTEMA RAG CONTESTAÇÕES
REM ═══════════════════════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo     Sistema RAG - Gerador de Contestações Jurídicas
echo ═══════════════════════════════════════════════════════════════════════════
echo.

REM Verificar se ambiente virtual existe
if not exist venv (
    echo ❌ ERRO: Ambiente virtual não encontrado.
    echo Execute primeiro: setup.bat
    pause
    exit /b 1
)

REM Ativar ambiente virtual
echo 📦 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Verificar .env
if not exist .env (
    echo.
    echo ⚠️  AVISO: Arquivo .env não encontrado!
    echo.
    echo Por favor:
    echo 1. Copie .env.example para .env
    echo 2. Adicione sua ANTHROPIC_API_KEY no arquivo .env
    echo.
    pause
    exit /b 1
)

REM Executar aplicação
echo.
echo 🚀 Iniciando aplicação...
echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo.

streamlit run app.py

pause
