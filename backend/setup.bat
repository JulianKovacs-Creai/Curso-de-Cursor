# ====== /backend/setup.bat (Windows) ======
@echo off
echo 🔧 Setting up E-commerce Backend (Legacy Version)...

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment  
echo 🔌 Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo 📥 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Initialize database
echo 🗄️ Initializing database...
python -c "from src.shared.database import init_db; init_db(); print('✅ Database initialized')"

echo 🎉 Backend setup completed successfully!
echo.
echo 🚀 To start the server:
echo   venv\Scripts\activate
echo   python main.py
echo.
echo 🌐 API will be available at:
echo   - Main API: http://localhost:8000
echo   - Swagger UI: http://localhost:8000/docs
echo   - ReDoc: http://localhost:8000/redoc
echo.
echo ⚠️  WARNING: This is legacy code with intentional vulnerabilities!
echo 📚 Ready for Day 1 refactoring!
pause

# ====================================


