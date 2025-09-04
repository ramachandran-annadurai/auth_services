from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routes.auth_routes import router as auth_router
from app.routes.admin_routes import router as admin_router
from app.utils.config import settings
from app.utils.exceptions import AuthServiceException
from app.utils.error_handler import (
    auth_service_exception_handler,
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler
)
import os

app = FastAPI(
    title="Patient Auth Service",
    description="Authentication service for patient management system",
    version="1.0.0"
)

# Add global exception handlers
app.add_exception_handler(AuthServiceException, auth_service_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(admin_router, prefix="/admin", tags=["administration"])

# Mount static files
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Auth Service"}

@app.get("/")
async def root():
    return {
        "service": "Patient Auth Service",
        "version": "1.0.0",
        "status": "running",
        "test_interface": "/test",
        "api_docs": "/docs"
    }

@app.get("/test")
async def test_interface():
    """Serve the test interface HTML page"""
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    index_file = os.path.join(static_dir, "index.html")
    
    if os.path.exists(index_file):
        return FileResponse(index_file)
    else:
        return {"error": "Test interface not found", "message": "HTML files not available"}
