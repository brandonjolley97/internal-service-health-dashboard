from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

class ServiceStatus(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    DEGRADED = "DEGRADED"
    MAINTENANCE = "MAINTENANCE"

class ServiceCreate(BaseModel):
    name: str = Field(
        ...,
        pattern=r"^[A-Za-z0-9-]+$", 
        description="Alphanumeric characters and dashes only", 
        examples=["email-notifier-v1"],
        min_length=1
    )
    description: str
    status: ServiceStatus

class ServiceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    status: ServiceStatus
    last_updated: datetime
    degraded_reason: str | None


class ServiceStatusUpdate(BaseModel):
    status: ServiceStatus
    reason: str | None = Field(
        default=None,
        description="Required when setting status to DEGRADED",
        min_length=1
    )