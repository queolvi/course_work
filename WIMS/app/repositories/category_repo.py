from typing import List, Optional

from app.models.category import Category

from app.repositories.base_repo import BaseRepository

class CategoryRepository(BaseRepository[Category]):

    def _map_row(self, row) -> Category:
        return Category(
            category_id=row.category_id,
            name=row.name,
            parent_id=row.parent_id,
        )

    def get_all(self) -> List[Category]:
        return self._fetch_all("SELECT category_id, name, parent_id FROM dbo.CATEGORIES")

    def get_by_id(self, category_id: int) -> Optional[Category]:
        return self._fetch_one(
            "SELECT category_id, name, parent_id FROM dbo.CATEGORIES WHERE category_id = ?",
            (category_id,),)

    def get_root_categories(self) -> List[Category]:
        return self._fetch_all(
            "SELECT category_id, name, parent_id FROM dbo.CATEGORIES WHERE parent_id IS NULL"
        )

    def create(self, name: str, parent_id: Optional[int] = None) -> int:
        cursor = self._execute(
            "INSERT INTO dbo.CATEGORIES (name, parent_id) OUTPUT INSERTED.category_id VALUES (?, ?)",
            (name, parent_id),)
        self.commit()
        return cursor.fetchone().category_id

    def delete(self, category_id: int) -> bool:
        cursor = self._execute("DELETE FROM dbo.CATEGORIES WHERE category_id = ?", (category_id,))
        self.commit()
        return cursor.rowcount > 0