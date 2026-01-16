from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceStatus, ServiceStatusUpdate
from app.domain.service_rules import validate_degraded_reason,validate_status_update

# Create
def create_service(db: Session, data: ServiceCreate) -> Service:

    if data.status == ServiceStatus.DEGRADED:
        validate_degraded_reason(data.status, None)

    service = Service(
        name = data.name,
        description=data.description,
        status = data.status.value,
        degraded_reason=None
    )

    db.add(service)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Service with this name already exists.")
    
    db.refresh(service)
    return service

# Read
def get_service(db: Session, service_id: int) -> Service | None:
    return db.get(Service, service_id)

# Read all
def list_services(db: Session) -> list[Service]:
    stmt = select(Service).order_by(Service.id)
    return db.execute(stmt).scalars().all()

# Update
def update_service_status(db: Session, service_id: int, update: ServiceStatusUpdate) -> Service | None:

    service = db.get(Service, service_id)
    if service is None:
        return None

    current_status = ServiceStatus(service.status)
    validate_status_update(current_status, update.status, update.reason)
    service.status = update.status.value

    if update.status == ServiceStatus.DEGRADED:
        service.degraded_reason = update.reason
    else:
        service.degraded_reason = None

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Database update failed.")
    
    db.refresh(service)
    return service

# Delete

