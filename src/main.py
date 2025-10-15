# src/main.py
import uvicorn
import asyncio
from .logger import setup_logger
from .api import app  # Import FastAPI app
from .config import EMBEDDING_MODEL, LLM  # Optional preload check

logger = setup_logger()

async def startup_tasks():
    """
    Run async startup tasks before starting the API.
    This can include preloading models, verifying connections, etc.
    """
    logger.info(" Initializing YouTube RAG Service components...")

    # Example: Verify LLM and embedding model load
    try:
        _ = EMBEDDING_MODEL
        _ = LLM
        logger.info("✅ Core models verified successfully.")
    except Exception as e:
        logger.error(f" Failed to initialize core models: {e}")
        raise e

    logger.info(" Startup tasks completed successfully.")

def run():
    """Start FastAPI using Uvicorn programmatically."""
    logger.info("🚀 Starting YouTube RAG API Service...")
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    asyncio.run(startup_tasks())
    run()
