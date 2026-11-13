from typing import List, Optional

from app.models.user import User
from app.repositories.base_repo import BaseRepository

class UserRepository(BaseRepository[User]):

    def _map_row(self, row) -> User:
        return User(
            user_id=row.user_id,
            username=row.username,
            password_hash=row.password_hash,
            full_name=row.full_name,
            role_id=row.role_id,
            is_active=bool(row.is_active),
            created_at=row.created_at,)

    def get_all(self) -> List[User]:
        return self._fetch_all(
            "SELECT user_id, username, password_hash, full_name, role_id, is_active, created_at "
            "FROM dbo.USERS")

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._fetch_one(
            "SELECT user_id, username, password_hash, full_name, role_id, is_active, created_at "
            "FROM dbo.USERS WHERE user_id = ?",
            (user_id,),)

    def get_by_username(self, username: str) -> Optional[User]:
        return self._fetch_one(
            "SELECT user_id, username, password_hash, full_name, role_id, is_active, created_at "
            "FROM dbo.USERS WHERE username = ?",
            (username,),)

    def create(
        self,
        username: str,
        password_hash: str,
        full_name: str,
        role_id: int,
        is_active: bool = True,
    ) -> int:
        cursor = self._execute(
            "INSERT INTO dbo.USERS (username, password_hash, full_name, role_id, is_active) "
            "OUTPUT INSERTED.user_id VALUES (?, ?, ?, ?, ?)",
            (username, password_hash, full_name, role_id, int(is_active)),)
        self.commit()
        return cursor.fetchone().user_id

    def update(self, user_id: int, full_name: str, role_id: int, is_active: bool) -> bool:
        cursor = self._execute(
            "UPDATE dbo.USERS SET full_name = ?, role_id = ?, is_active = ? WHERE user_id = ?",
            (full_name, role_id, int(is_active), user_id),
        )
        self.commit()
        return cursor.rowcount > 0

    def delete(self, user_id: int) -> bool:
        cursor = self._execute("DELETE FROM dbo.USERS WHERE user_id = ?", (user_id,))
        self.commit()
        return cursor.rowcount > 0