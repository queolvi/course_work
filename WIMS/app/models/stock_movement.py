from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

class stock_movement_type(Enum):
    receipt
    shipment
    write_off
    adjustment

@dataclass
class StockMovement:
    movement_id: int
    batch_id: int
    type: Optional[stock_movement_type] = None  
    quantity: int
    user_id: int
    document_id: Optional[int] = None
    created_at: Optional[datetime] = None

    def __str__(self) -> str:
        return (
            f"Movement(id={self.movement_id}, batch={self.batch_id}, "
            f"type={self.type}, qty={self.quantity})"
        )