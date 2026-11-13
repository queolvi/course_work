from datetime import date
from typing import List, Optional

from app.models.batch import Batch
from app.repositories.base_repo import BaseRepository


class BatchRepository(BaseRepository[Batch]):

    def _map_row(self, row) -> Batch:
        return Batch(
            batch_id=row.batch_id,
            product_id=row.product_id,
            quantity=row.quantity,
            reserved_quantity=row.reserved_quantity,
            manufacture_date=row.manufacture_date,
            expiration_date=row.expiration_date,
            location_id=row.location_id,
            created_at=row.created_at,)

    def get_all(self) -> List[Batch]:
        return self._fetch_all(
            "SELECT batch_id, product_id, quantity, reserved_quantity, "
            "manufacture_date, expiration_date, location_id, created_at "
            "FROM dbo.BATCHES")

    def get_by_id(self, batch_id: int) -> Optional[Batch]:
        return self._fetch_one(
            "SELECT batch_id, product_id, quantity, reserved_quantity, "
            "manufacture_date, expiration_date, location_id, created_at "
            "FROM dbo.BATCHES WHERE batch_id = ?",
            (batch_id,),)

    def get_by_product(self, product_id: int) -> List[Batch]:
        return self._fetch_all(
            "SELECT batch_id, product_id, quantity, reserved_quantity, "
            "manufacture_date, expiration_date, location_id, created_at "
            "FROM dbo.BATCHES WHERE product_id = ?",
            (product_id,),)

    def get_available_by_product(self, product_id: int) -> List[Batch]:
        return self._fetch_all(
            "SELECT batch_id, product_id, quantity, reserved_quantity, "
            "manufacture_date, expiration_date, location_id, created_at "
            "FROM dbo.BATCHES "
            "WHERE product_id = ? AND (quantity - reserved_quantity) > 0",
            (product_id,),)

    def get_fefo_batches(self, product_id: int) -> List[Batch]:
        return self._fetch_all(
            "SELECT batch_id, product_id, quantity, reserved_quantity, "
            "manufacture_date, expiration_date, location_id, created_at "
            "FROM dbo.BATCHES "
            "WHERE product_id = ? AND (quantity - reserved_quantity) > 0 "
            "  AND expiration_date >= CAST(GETDATE() AS DATE) "
            "ORDER BY expiration_date ASC, manufacture_date ASC",
            (product_id,),)

    def get_expired_batches(self) -> List[Batch]:
        return self._fetch_all(
            "SELECT batch_id, product_id, quantity, reserved_quantity, "
            "manufacture_date, expiration_date, location_id, created_at "
            "FROM dbo.BATCHES "
            "WHERE expiration_date < CAST(GETDATE() AS DATE)",)

    def get_expiring_soon(self, days: int = 7) -> List[Batch]:
        return self._fetch_all(
            "SELECT batch_id, product_id, quantity, reserved_quantity, "
            "manufacture_date, expiration_date, location_id, created_at "
            "FROM dbo.BATCHES "
            "WHERE expiration_date BETWEEN CAST(GETDATE() AS DATE) "
            "  AND DATEADD(day, ?, CAST(GETDATE() AS DATE))",
            (days,),)

    def create(
        self,
        product_id: int,
        quantity: int,
        manufacture_date: date,
        expiration_date: date,
        location_id: int,
        reserved_quantity: int = 0,
    ) -> int:
        cursor = self._execute(
            "INSERT INTO dbo.BATCHES "
            "(product_id, quantity, reserved_quantity, manufacture_date, expiration_date, location_id) "
            "OUTPUT INSERTED.batch_id VALUES (?, ?, ?, ?, ?, ?)",
            (product_id, quantity, reserved_quantity, manufacture_date, expiration_date, location_id),
        )
        self.commit()
        return cursor.fetchone().batch_id

    def update_quantity(self, batch_id: int, new_quantity: int) -> bool:
        cursor = self._execute(
            "UPDATE dbo.BATCHES SET quantity = ? WHERE batch_id = ?",
            (new_quantity, batch_id),)
        self.commit()
        return cursor.rowcount > 0

    def increase_reserved(self, batch_id: int, amount: int) -> bool:
        cursor = self._execute(
            "UPDATE dbo.BATCHES SET reserved_quantity = reserved_quantity + ? "
            "WHERE batch_id = ? AND (quantity - reserved_quantity) >= ?",
            (amount, batch_id, amount),
        )
        self.commit()
        return cursor.rowcount > 0

    def decrease_reserved(self, batch_id: int, amount: int) -> bool:
        cursor = self._execute(
            "UPDATE dbo.BATCHES SET reserved_quantity = reserved_quantity - ? "
            "WHERE batch_id = ? AND reserved_quantity >= ?",
            (amount, batch_id, amount),
        )
        self.commit()
        return cursor.rowcount > 0

    def delete(self, batch_id: int) -> bool:
        cursor = self._execute("DELETE FROM dbo.BATCHES WHERE batch_id = ?", (batch_id,))
        self.commit()
        return cursor.rowcount > 0