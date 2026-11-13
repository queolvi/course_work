from typing import List, Optional

from app.models.storage_location import StorageLocation
from app.repositories.base_repo import BaseRepository


class StorageLocationRepository(BaseRepository[StorageLocation]):

    def _map_row(self, row) -> StorageLocation:
        return StorageLocation(
            location_id=row.location_id,
            warehouse_name=row.warehouse_name,
            zone=row.zone,
            shelf=row.shelf,
            cell=row.cell,
            description=row.description,)

    def get_all(self) -> List[StorageLocation]:
        return self._fetch_all(
            "SELECT location_id, warehouse_name, zone, shelf, cell, description "
            "FROM dbo.STORAGE_LOCATIONS")

    def get_by_id(self, location_id: int) -> Optional[StorageLocation]:
        return self._fetch_one(
            "SELECT location_id, warehouse_name, zone, shelf, cell, description "
            "FROM dbo.STORAGE_LOCATIONS WHERE location_id = ?",(location_id,),)

    def create(
        self,
        warehouse_name: str,
        zone: str,
        shelf: str,
        cell: str,
        description: Optional[str] = None,
    ) -> int:
        cursor = self._execute(
            "INSERT INTO dbo.STORAGE_LOCATIONS (warehouse_name, zone, shelf, cell, description) "
            "OUTPUT INSERTED.location_id VALUES (?, ?, ?, ?, ?)",
            (warehouse_name, zone, shelf, cell, description),)
        self.commit()
        return cursor.fetchone().location_id

    def delete(self, location_id: int) -> bool:
        cursor = self._execute("DELETE FROM dbo.STORAGE_LOCATIONS WHERE location_id = ?", (location_id,))
        self.commit()
        return cursor.rowcount > 0