from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.routes.services import router as services_router

app = FastAPI()
app.include_router(services_router)

@app.get("/health")
def health():
    
    return {"status": "ok"}

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):

    db.execute(text("Select 1"))

    return {"db": "ok"}