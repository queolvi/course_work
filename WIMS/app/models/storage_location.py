from dataclasses import dataclass
from typing import Optional


@dataclass
class StorageLocation:
    location_id: int
    warehouse_name: str
    zone: str
    shelf: str
    cell: str
    description: Optional[str] = None

    def __str__(self) -> str:
        return f"Location(id={self.location_id},{self.warehouse_name}/{self.zone}/{self.shelf}/{self.cell})"