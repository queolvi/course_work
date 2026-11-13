from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    user_id: int
    username: str
    password_hash: str
    full_name: str
    role_id: int
    is_active: bool = True
    created_at: Optional[datetime] = None

    def __str__(self) -> str:
        return f"User(id={self.user_id}, username={self.username}, active={self.is_active})"