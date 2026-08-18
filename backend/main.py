#TODO: Dependency Injection, Seperate Modules from running execution, transparent audit, logging, Keeping core business logic pure and decoupled from entry mechanisms
import logging
from fastapi import FastAPI
from src.interfaces.api import router

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="My Awesome API",
    version="1.0.0"
)   

app.include_router(router)

@app.get("/api")
async def api_root():
    logger.info("API root endpoint hit")
    return {"status": "running", "version": "1.0.0"}