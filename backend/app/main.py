from fastapi import FastAPI
from app.api import document_router
from app.adapters.postgres.database import Base, engine

app = FastAPI(title="barkibu-api", version="0.1.0")
app.include_router(document_router.router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok"}
