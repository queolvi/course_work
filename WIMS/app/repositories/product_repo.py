from typing import List, Optional

from app.models.product import Product
from app.repositories.base_repo import BaseRepository


class ProductRepository(BaseRepository[Product]):

    def _map_row(self, row) -> Product:
        return Product(
            product_id=row.product_id,
            name=row.name,
            stock_keeping_unit=row.stock_keeping_unit,
            category_id=row.category_id,
            unit=row.unit,
            description=row.description,
            min_stock=row.min_stock,
        )

    def get_all(self) -> List[Product]:
        return self._fetch_all(
            "SELECT product_id, name, stock_keeping_unit, category_id, unit, description, min_stock "
            "FROM dbo.PRODUCTS")

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self._fetch_one(
            "SELECT product_id, name, stock_keeping_unit, category_id, unit, description, min_stock "
            "FROM dbo.PRODUCTS WHERE product_id = ?",
            (product_id,),)

    def get_by_sku(self, sku: str) -> Optional[Product]:
        return self._fetch_one(
            "SELECT product_id, name, stock_keeping_unit, category_id, unit, description, min_stock "
            "FROM dbo.PRODUCTS WHERE stock_keeping_unit = ?",
            (sku,),)

    def get_by_category(self, category_id: int) -> List[Product]:
        return self._fetch_all(
            "SELECT product_id, name, stock_keeping_unit, category_id, unit, description, min_stock "
            "FROM dbo.PRODUCTS WHERE category_id = ?",
            (category_id,),)

    def create(
        self,
        name: str,
        sku: str,
        category_id: int,
        unit: str,
        description: Optional[str] = None,
        min_stock: int = 0,
    ) -> int:
        cursor = self._execute(
            "INSERT INTO dbo.PRODUCTS (name, stock_keeping_unit, category_id, unit, description, min_stock) "
            "OUTPUT INSERTED.product_id VALUES (?, ?, ?, ?, ?, ?)",
            (name, sku, category_id, unit, description, min_stock),)
        self.commit()
        return cursor.fetchone().product_id

    def update(
        self,
        product_id: int,
        name: str,
        unit: str,
        description: Optional[str],
        min_stock: int,
    ) -> bool:
        cursor = self._execute(
            "UPDATE dbo.PRODUCTS SET name = ?, unit = ?, description = ?, min_stock = ? "
            "WHERE product_id = ?",
            (name, unit, description, min_stock, product_id),
        )
        self.commit()
        return cursor.rowcount > 0

    def delete(self, product_id: int) -> bool:
        cursor = self._execute("DELETE FROM dbo.PRODUCTS WHERE product_id = ?", (product_id,))
        self.commit()
        return cursor.rowcount > 0