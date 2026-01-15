from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.schemas.service import ServiceRead, ServiceStatusUpdate, ServiceCreate
from app.crud import service as service_crud
from app.db.session import get_db

router = APIRouter(
    prefix="/services",
    tags=["services"]
)

@router.get("", response_model=List[ServiceRead])
def list_services_route(db: Session = Depends(get_db)):
    return service_crud.list_services(db)

@router.get("/{service_id}", response_model=ServiceRead)
def get_service_route(service_id: int, db: Session=Depends(get_db)):
    service = service_crud.get_service(db, service_id)

    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    
    return service

@router.post("",response_model=ServiceRead, status_code=status.HTTP_201_CREATED)
def create_service_route(payload: ServiceCreate, db: Session=Depends(get_db)):
    try:
        service = service_crud.create_service(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return service

@router.put("/{service_id}/status", response_model=ServiceRead)
def update_service_status_route(service_id: int, payload: ServiceStatusUpdate, db: Session=Depends(get_db)):
    try:
        service = service_crud.update_service_status(db, service_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    
    return service