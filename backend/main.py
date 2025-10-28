from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from src.products.api import router as products_router
from src.shared.database import init_db

# ❌ PROBLEMA: Configuración muy básica sin validación
app = FastAPI(
    title="E-commerce Legacy API",
    description="Legacy e-commerce API that needs refactoring",
    version="0.1.0",
    # ❌ PROBLEMA: No configuración de seguridad
)

# ❌ PROBLEMA: CORS muy permisivo - security issue
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ❌ Muy permisivo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ❌ PROBLEMA: No middleware de logging, no rate limiting, no security headers

# Include routers
app.include_router(products_router)

@app.get("/", tags=["General"])
async def root():
    """Root endpoint - basic health check"""
    return {
        "message": "E-commerce Legacy API",
        "status": "running",
        "version": "0.1.0"
    }

@app.get("/health", tags=["General"])
async def health_check():
    """Basic health check endpoint"""
    return {"status": "ok", "message": "API is running"}

if __name__ == "__main__":
    # Initialize database on startup
    print("🔧 Initializing database...")
    init_db()
    print("✅ Database initialized")
    
    # ❌ PROBLEMA: No configuración de production, no logging setup
    print("🚀 Starting E-commerce Legacy API...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # ❌ PROBLEMA: reload=True hardcodeado
        # ❌ PROBLEMA: No configuración de workers, no SSL
    )


