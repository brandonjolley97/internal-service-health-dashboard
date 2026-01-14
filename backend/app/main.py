from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

app = FastAPI()

@app.get("/health")
def health():
    
    return {"status": "ok"}

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):

    db.execute(text("Select 1"))

    return {"db": "ok"}