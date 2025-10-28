# ====== /backend/setup.sh (Linux/Mac) ======
#!/bin/bash

echo "🔧 Setting up E-commerce Backend (Legacy Version)..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
echo "🗄️ Initializing database..."
python -c "
from src.shared.database import init_db
try:
    init_db()
    print('✅ Database initialized successfully')
except Exception as e:
    print(f'❌ Error initializing database: {e}')
    exit(1)
"
echo "🎉 Backend setup completed successfully!"
echo ""
echo "🚀 To start the server:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "🌐 API will be available at:"
echo "  - Main API: http://localhost:8000"
echo "  - Swagger UI: http://localhost:8000/docs"
echo "  - ReDoc: http://localhost:8000/redoc"
echo ""
echo "⚠️  WARNING: This is legacy code with intentional vulnerabilities!"
echo "📚 Ready for Day 1 refactoring!"

# ====================================

