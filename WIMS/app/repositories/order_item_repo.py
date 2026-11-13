from decimal import Decimal
from typing import List, Optional

from app.models.order_item import OrderItem
from app.repositories.base_repo import BaseRepository


class OrderItemRepository(BaseRepository[OrderItem]):
    def _map_row(self, row) -> OrderItem:
        return OrderItem(
            order_item_id=row.order_item_id,
            order_id=row.order_id,
            batch_id=row.batch_id,
            quantity=row.quantity,
            price=Decimal(str(row.price)),)

    def get_by_order(self, order_id: int) -> List[OrderItem]:
        return self._fetch_all(
            "SELECT order_item_id, order_id, batch_id, quantity, price "
            "FROM dbo.ORDER_ITEMS WHERE order_id = ?",(order_id,),
        )

    def create(self, order_id: int, batch_id: int, quantity: int, price: Decimal) -> int:
        cursor = self._execute(
            "INSERT INTO dbo.ORDER_ITEMS (order_id, batch_id, quantity, price) "
            "OUTPUT INSERTED.order_item_id VALUES (?, ?, ?, ?)",
            (order_id, batch_id, quantity, float(price)),)
        self.commit()
        return cursor.fetchone().order_item_id

    def delete(self, order_item_id: int) -> bool:
        cursor = self._execute(
            "DELETE FROM dbo.ORDER_ITEMS WHERE order_item_id = ?", (order_item_id,))
        self.commit()
        return cursor.rowcount > 0