#TODO: Dependency Injection, Seperate Modules from running execution, transparent audit, logging, Keeping core business logic pure and decoupled from entry mechanisms
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.presentation.api.v1 import router
from src.common.logger import setup_logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="My Awesome API",
    version="1.0.0",
)   

app.include_router(router)

@app.get("/api")
async def api_root():
    logging.getLogger(__name__).info("API root endpoint hit")
    return {"status": "running", "version": "1.0.0"}