from dataclasses import dataclass
from typing import Optional


@dataclass
class Customer:
    customer_id: int
    name: str
    contact: str
    user_id: Optional[int] = None
    inn: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    building: Optional[str] = None
    apartment: Optional[str] = None

    def __str__(self) -> str:
        return f"Customer(id={self.customer_id}, name={self.name})"