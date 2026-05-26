#!/usr/bin/env python3
"""
Xianyu Auto Reply - Backend Web Server
Main entry point for the FastAPI application.
"""

import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown events."""
    logger.info("Starting Xianyu Auto Reply backend...")
    # TODO: Initialize database connection, scheduler, etc.
    yield
    logger.info("Shutting down Xianyu Auto Reply backend...")
    # TODO: Cleanup resources


app = FastAPI(
    title="Xianyu Auto Reply",
    description="Automated reply system for Xianyu (闲鱼) platform",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {"status": "ok", "message": "Xianyu Auto Reply API is running"}


@app.get("/health")
async def health_check():
    """Health check endpoint for Docker/load balancer."""
    return {"status": "healthy"}


# Import and include routers
# from routers import auth, messages, rules, accounts
# app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
# app.include_router(messages.router, prefix="/api/messages", tags=["messages"])
# app.include_router(rules.router, prefix="/api/rules", tags=["rules"])
# app.include_router(accounts.router, prefix="/api/accounts", tags=["accounts"])


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "false").lower() == "true"

    logger.info(f"Starting server on {host}:{port} (debug={debug})")
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="debug" if debug else "info",
    )
