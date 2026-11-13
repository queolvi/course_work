from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

class reservations_statuses(Enum):
    active
    fulfilled
    cancelled
    
@dataclass
class Reservation:
    reservation_id: int
    batch_id: int
    user_id: int
    quantity: int
    status: Optional[reservations_statuses] = active
    expires_at: Optional[datetime] = None
    order_id: Optional[int] = None
    created_at: Optional[datetime] = None

    @property
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at

    def __str__(self) -> str:
        return (
            f"Reservation(id={self.reservation_id}, batch={self.batch_id}, "
            f"qty={self.quantity}, status={self.status})"
        )