# ====== /backend/start.sh (Linux/Mac) ======
#!/bin/bash

echo "🚀 Starting E-commerce Backend (Legacy Version)..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "🔧 Please run setup.sh first"
    exit 1
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Check if database exists
if [ ! -f "ecommerce.db" ]; then
    echo "🗄️ Database not found, initializing..."
    python -c "from src.shared.database import init_db; init_db()"
fi

# Start the server
echo "🌟 Starting FastAPI server..."
echo "🌐 API will be available at: http://localhost:8000"
echo "📚 Swagger UI: http://localhost:8000/docs"
echo ""
echo "⚠️  WARNING: This code contains intentional vulnerabilities!"
echo "🎯 Ready for Clean Architecture refactoring!"
echo ""
echo "Press Ctrl+C to stop the server"

python main.py

# ====================================


