from dataclasses import dataclass
from typing import Optional


@dataclass
class Category:
    category_id: int
    name: str
    parent_id: Optional[int] = None

    def __str__(self) -> str:
        return f"Category(id={self.category_id}, name={self.name})"