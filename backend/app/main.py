from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from app.db.session import get_db
from app.api.routes.services import router as services_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.seed import seed_services
    seed_services()
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(services_router)


@app.get("/health")
def health():
    
    return {"status": "ok"}

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):

    db.execute(text("Select 1"))

    return {"db": "ok"}

