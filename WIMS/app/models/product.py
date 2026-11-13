from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    product_id: int
    name: str
    stock_keeping_unit: str
    category_id: int
    unit: str 
    description: Optional[str] = None
    min_stock: int = 0

    def __str__(self) -> str:
        return f"Product(id={self.product_id}, sku={self.stock_keeping_unit}, name={self.name})"