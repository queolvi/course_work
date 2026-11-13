from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class Batch:
    batch_id: int
    product_id: int
    quantity: int
    reserved_quantity: int
    manufacture_date: date
    expiration_date: date
    location_id: int
    created_at: Optional[datetime] = None

    @property
    def available_quantity(self) -> int:
        return self.quantity - self.reserved_quantity

    @property
    def is_expired(self) -> bool:
        return self.expiration_date < date.today()

    @property
    def days_until_expiration(self) -> int:
        return (self.expiration_date - date.today()).days

    def __str__(self) -> str:
        return (
            f"Batch(id={self.batch_id}, product_id={self.product_id}, "
            f"qty={self.quantity}, reserved={self.reserved_quantity}, "
            f"exp={self.expiration_date})"
        )