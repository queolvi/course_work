from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum
class order_statuses(Enum):
    new = "new"
    processing = "processing"
    completed = "completed"
    cancelled = "cancelled"
    
@dataclass
class Order:
    order_id: int
    customer_id: int
    user_id: int
    status: order_statuses = order_statuses.new
    created_at: Optional[datetime] = None

    def __str__(self) -> str:
        return f"Order(id={self.order_id}, status={self.status})"