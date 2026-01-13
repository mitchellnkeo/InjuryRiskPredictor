"""
FastAPI Main Application

Injury Risk Predictor API Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .models import HealthResponse
from .routers import predictions

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Injury Risk Predictor API",
    description="API for predicting injury risk from training data using ACWR and ML models",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        # Add production frontend URL here when deployed
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predictions.router)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Injury Risk Predictor API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns API status and whether ML model is loaded.
    """
    try:
        from .ml.predictor import get_predictor
        predictor = get_predictor()
        model_loaded = predictor.model is not None and predictor.scaler is not None
        
        return HealthResponse(
            status="healthy",
            model_loaded=model_loaded,
            version="1.0.0"
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}", exc_info=True)
        return HealthResponse(
            status="unhealthy",
            model_loaded=False,
            version="1.0.0"
        )


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting Injury Risk Predictor API...")
    try:
        from .ml.predictor import get_predictor
        predictor = get_predictor()
        logger.info("✓ Model loaded successfully")
        logger.info(f"✓ Model type: {type(predictor.model).__name__}")
    except Exception as e:
        logger.error(f"Failed to load model on startup: {e}")
        logger.warning("API will start but predictions may fail")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Injury Risk Predictor API...")
