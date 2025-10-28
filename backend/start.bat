# ====== /backend/start.bat (Windows) ======
@echo off
echo 🚀 Starting E-commerce Backend (Legacy Version)...

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo 🔧 Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate

REM Check if database exists
if not exist "ecommerce.db" (
    echo 🗄️ Database not found, initializing...
    python -c "from src.shared.database import init_db; init_db()"
)

REM Start the server
echo 🌟 Starting FastAPI server...
echo 🌐 API will be available at: http://localhost:8000
echo 📚 Swagger UI: http://localhost:8000/docs
echo.
echo ⚠️  WARNING: This code contains intentional vulnerabilities!
echo 🎯 Ready for Clean Architecture refactoring!
echo.
echo Press Ctrl+C to stop the server

python main.py


