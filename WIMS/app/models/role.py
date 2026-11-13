from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Role:
    role_id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None

    def __str__(self) -> str:
        return f"Role(id={self.role_id}, name={self.name})"