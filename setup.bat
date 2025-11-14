@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM SCRIPT DE SETUP - SISTEMA RAG CONTESTAÇÕES
REM ═══════════════════════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo     SETUP - Sistema RAG Geração de Contestações Jurídicas
echo ═══════════════════════════════════════════════════════════════════════════
echo.

REM Verificar Python
echo [1/6] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Python não encontrado. Instale Python 3.10+ primeiro.
    pause
    exit /b 1
)
python --version
echo ✅ Python encontrado
echo.

REM Criar ambiente virtual
echo [2/6] Criando ambiente virtual...
if exist venv (
    echo ⚠️  Ambiente virtual já existe. Pulando criação.
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ❌ ERRO ao criar ambiente virtual
        pause
        exit /b 1
    )
    echo ✅ Ambiente virtual criado
)
echo.

REM Ativar ambiente virtual
echo [3/6] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ ERRO ao ativar ambiente virtual
    pause
    exit /b 1
)
echo ✅ Ambiente virtual ativado
echo.

REM Atualizar pip
echo [4/6] Atualizando pip...
python -m pip install --upgrade pip --quiet
echo ✅ pip atualizado
echo.

REM Instalar dependências
echo [5/6] Instalando dependências...
echo Este processo pode levar alguns minutos...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ ERRO ao instalar dependências
    pause
    exit /b 1
)
echo ✅ Dependências instaladas
echo.

REM Criar .env
echo [6/6] Configurando ambiente...
if exist .env (
    echo ⚠️  Arquivo .env já existe. Não será sobrescrito.
) else (
    if exist .env.example (
        copy .env.example .env >nul
        echo ✅ Arquivo .env criado a partir de .env.example
        echo.
        echo ⚠️  IMPORTANTE: Edite o arquivo .env e adicione sua ANTHROPIC_API_KEY
        echo    Caminho: %CD%\.env
    ) else (
        echo ⚠️  Arquivo .env.example não encontrado
    )
)
echo.

REM Criar diretórios
echo Criando diretórios de output...
if not exist outputs mkdir outputs
if not exist logs mkdir logs
if not exist temp mkdir temp
echo ✅ Diretórios criados
echo.

echo ═══════════════════════════════════════════════════════════════════════════
echo     ✅ SETUP CONCLUÍDO COM SUCESSO!
echo ═══════════════════════════════════════════════════════════════════════════
echo.
echo 📋 PRÓXIMOS PASSOS:
echo.
echo 1. Edite o arquivo .env e adicione sua ANTHROPIC_API_KEY:
echo    - Abra: %CD%\.env
echo    - Adicione: ANTHROPIC_API_KEY=sk-ant-api03-...
echo.
echo 2. Execute a aplicação:
echo    - streamlit run app.py
echo.
echo 3. Acesse no navegador:
echo    - http://localhost:8501
echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo.

pause
