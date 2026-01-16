from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.service import Service

DEFAULT_SERVICES = [
    {
        "name": "database-scraper",
        "description": "Scrapes and syncs internal metadata",
        "status": "ONLINE"
    },
    {
        "name": "email-notifier-1",
        "description": "Sends alert emails to users",
        "status": "OFFLINE"
    },
    {
        "name": "analytics_engine",
        "description": "Processes events",
        "status": "MAINTENANCE"
    }
]

def seed_services():
    db: Session = SessionLocal()
    
    try:
        for s in DEFAULT_SERVICES:
            exists = db.query(Service).filter(Service.name == s["name"]).first()
            if exists is not None:
                continue
            
            db.add(Service(
                name=s["name"],
                description=s["description"],
                status=s["status"],
                degraded_reason=None
            ))
        db.commit()
    finally:
        db.close()