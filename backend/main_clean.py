"""
Main Application - Clean Architecture Implementation.

This is the new main.py file that uses Clean Architecture principles.
It replaces the legacy main.py with proper separation of concerns,
dependency injection, and scalable architecture.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from contextlib import asynccontextmanager

from src.shared.config import get_settings, is_development
from src.shared.database import initialize_database, check_database_health
from src.products.infrastructure.api import router as products_router
from src.auth.infrastructure.api import router as auth_router
from src.auth.infrastructure.user_repository import SQLiteUserRepository

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events for the application.
    """
    # Startup
    logger.info("🚀 Starting Clean Architecture E-commerce API...")
    
    try:
        # Initialize database
        logger.info("🔧 Initializing database...")
        initialize_database()
        
        # Initialize auth tables by creating user repository instance
        settings = get_settings()
        user_repo = SQLiteUserRepository(settings.database_url)
        logger.info("✅ Auth tables initialized")
        
        logger.info("✅ Database initialized successfully")
        
        # Check database health
        health_status = check_database_health()
        if health_status["status"] == "healthy":
            logger.info("✅ Database health check passed")
        else:
            logger.warning(f"⚠️  Database health check failed: {health_status}")
        
        logger.info("✅ Application startup completed")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Clean Architecture E-commerce API...")


# Create FastAPI application with Clean Architecture
settings = get_settings()

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url="/docs" if is_development() else None,
    redoc_url="/redoc" if is_development() else None,
    lifespan=lifespan
)

# Configure CORS with proper security
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Include routers
app.include_router(products_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")


# Health check endpoints
@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Clean Architecture E-commerce API",
        "version": settings.api_version,
        "status": "running",
        "environment": settings.environment,
        "docs_url": "/docs" if is_development() else None
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Comprehensive health check endpoint.
    """
    try:
        # Check database health
        db_health = check_database_health()
        
        health_status = {
            "status": "healthy" if db_health["status"] == "healthy" else "unhealthy",
            "timestamp": "2024-01-01T00:00:00Z",  # You can use datetime.now().isoformat()
            "version": settings.api_version,
            "environment": settings.environment,
            "database": db_health
        }
        
        if health_status["status"] == "unhealthy":
            return JSONResponse(
                status_code=503,
                content=health_status
            )
        
        return health_status
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": "2024-01-01T00:00:00Z"
            }
        )


@app.get("/api/v1/status", tags=["Health"])
async def api_status():
    """
    API status endpoint for monitoring.
    """
    return {
        "api": "Clean Architecture E-commerce API",
        "version": settings.api_version,
        "status": "operational",
        "environment": settings.environment,
        "features": [
            "Products Management",
            "Clean Architecture",
            "Repository Pattern",
            "Domain-Driven Design",
            "Dependency Injection"
        ]
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "type": "InternalServerError"
        }
    )


if __name__ == "__main__":
    # Run the application
    logger.info(f"🌍 Starting server on {settings.host}:{settings.port}")
    logger.info(f"🔧 Environment: {settings.environment}")
    logger.info(f"🐛 Debug mode: {settings.debug}")
    
    uvicorn.run(
        "main_clean:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload and is_development(),
        log_level=settings.log_level.lower(),
        access_log=True
    )
