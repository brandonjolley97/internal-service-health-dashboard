from app.schemas.service import ServiceStatus


def validate_status_update(current_status: ServiceStatus, new_status: ServiceStatus, reason: str | None) -> None:
    validate_status_transition(current_status, new_status)
    validate_degraded_reason(new_status, reason)

def validate_status_transition(current_status: ServiceStatus, new_status: ServiceStatus) -> None:

    if current_status == ServiceStatus.OFFLINE and new_status == ServiceStatus.ONLINE:
        raise ValueError("OFFLINE services must go to MAINTENANCE before ONLINE.")

def validate_degraded_reason(new_status: ServiceStatus, reason: str | None) -> None:

    if new_status == ServiceStatus.DEGRADED:
        if reason is None or reason.strip() == "":
            raise ValueError("Reason is required when setting status to DEGRADED.")