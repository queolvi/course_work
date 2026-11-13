from dataclasses import dataclass
from decimal import Decimal


@dataclass
class OrderItem:
    order_item_id: int
    order_id: int
    batch_id: int
    quantity: int
    price: Decimal

    def __str__(self) -> str:
        return f"OrderItem(id={self.order_item_id}, batch={self.batch_id}, qty={self.quantity})"