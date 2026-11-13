from typing import List, Optional

from app.models.order import order_statuses
from app.models.order import Order

from app.repositories.base_repo import BaseRepository


class OrderRepository(BaseRepository[Order]):

    def _map_row(self, row) -> Order:
        return Order(
            order_id=row.order_id,
            customer_id=row.customer_id,
            user_id=row.user_id,
            status=row.status,
            created_at=row.created_at,)

    def get_all(self) -> List[Order]:
        return self._fetch_all("SELECT order_id, customer_id, user_id, status, created_at FROM dbo.ORDERS")

    def get_by_id(self, order_id: int) -> Optional[Order]:
        return self._fetch_one(
            "SELECT order_id, customer_id, user_id, status, created_at "
            "FROM dbo.ORDERS WHERE order_id = ?",(order_id,),)

    def get_by_customer(self, customer_id: int) -> List[Order]:
        return self._fetch_all(
            "SELECT order_id, customer_id, user_id, status, created_at "
            "FROM dbo.ORDERS WHERE customer_id = ?",(customer_id,),)

    def create(self, customer_id: int, user_id: int, status: order_statuses = "new") -> int:
        cursor = self._execute(
            "INSERT INTO dbo.ORDERS (customer_id, user_id, status) "
            "OUTPUT INSERTED.order_id VALUES (?, ?, ?)",(customer_id, user_id, status),)
        self.commit()
        return cursor.fetchone().order_id

    def update_status(self, order_id: int, status: order_statuses) -> bool:
        cursor = self._execute(
            "UPDATE dbo.ORDERS SET status = ? WHERE order_id = ?",(status, order_id),)
        self.commit()
        return cursor.rowcount > 0

    def delete(self, order_id: int) -> bool:
        cursor = self._execute("DELETE FROM dbo.ORDERS WHERE order_id = ?", (order_id,))
        self.commit()
        return cursor.rowcount > 0