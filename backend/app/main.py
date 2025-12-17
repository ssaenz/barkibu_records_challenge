import logging
from fastapi import FastAPI
from app.api import document_router
from app.adapters.postgres.database import Base, engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(title="barkibu-api", version="0.1.0")
app.include_router(document_router.router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok"}
