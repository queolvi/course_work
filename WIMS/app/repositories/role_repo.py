from typing import List, Optional

from app.models.role import Role
from app.repositories.base_repo import BaseRepository


class RoleRepository(BaseRepository[Role]):

    def _map_row(self, row) -> Role:
        return Role(
            role_id=row.role_id,
            name=row.name,
            description=row.description,
            created_at=row.created_at,
        )

    def get_all(self) -> List[Role]:
        return self._fetch_all("SELECT role_id, name, description, created_at FROM dbo.ROLES")

    def get_by_id(self, role_id: int) -> Optional[Role]:
        return self._fetch_one(
            "SELECT role_id, name, description, created_at FROM dbo.ROLES WHERE role_id = ?",
            (role_id,),
        )

    def get_by_name(self, name: str) -> Optional[Role]:
        return self._fetch_one(
            "SELECT role_id, name, description, created_at FROM dbo.ROLES WHERE name = ?",
            (name,),
        )

    def create(self, name: str, description: Optional[str] = None) -> int:
        cursor = self._execute(
            "INSERT INTO dbo.ROLES (name, description) OUTPUT INSERTED.role_id VALUES (?, ?)",
            (name, description),
        )
        self.commit()
        return cursor.fetchone().role_id

    def delete(self, role_id: int) -> bool:
        cursor = self._execute("DELETE FROM dbo.ROLES WHERE role_id = ?", (role_id,))
        self.commit()
        return cursor.rowcount > 0