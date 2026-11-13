from typing import List, Optional

from app.models.stock_movement import stock_movement_type
from app.models.stock_movement import StockMovement

from app.repositories.base_repo import BaseRepository


class StockMovementRepository(BaseRepository[StockMovement]):
    def _map_row(self, row) -> StockMovement:
        return StockMovement(
            movement_id=row.movement_id,
            batch_id=row.batch_id,
            type=row.type,
            quantity=row.quantity,
            user_id=row.user_id,
            document_id=row.document_id,
            created_at=row.created_at,)

    def get_all(self) -> List[StockMovement]:
        return self._fetch_all(
            "SELECT movement_id, batch_id, type, quantity, user_id, document_id, created_at "
            "FROM dbo.STOCK_MOVEMENTS ORDER BY created_at DESC")

    def get_by_batch(self, batch_id: int) -> List[StockMovement]:
        return self._fetch_all(
            "SELECT movement_id, batch_id, type, quantity, user_id, document_id, created_at "
            "FROM dbo.STOCK_MOVEMENTS WHERE batch_id = ? ORDER BY created_at DESC",(batch_id,),
        )

    def get_by_type(self, movement_type: stock_movement_type) -> List[StockMovement]:
        return self._fetch_all(
            "SELECT movement_id, batch_id, type, quantity, user_id, document_id, created_at "
            "FROM dbo.STOCK_MOVEMENTS WHERE type = ? ORDER BY created_at DESC",(movement_type,),
        )

    def create(
        self,
        batch_id: int,
        movement_type: stock_movement_type,
        quantity: int,
        user_id: int,
        document_id: Optional[int] = None,) -> int:
        cursor = self._execute(
            "INSERT INTO dbo.STOCK_MOVEMENTS (batch_id, type, quantity, user_id, document_id) "
            "OUTPUT INSERTED.movement_id VALUES (?, ?, ?, ?, ?)",
            (batch_id, movement_type, quantity, user_id, document_id),)
        self.commit()
        return cursor.fetchone().movement_id

    def delete(self, movement_id: int) -> bool:
        cursor = self._execute(
            "DELETE FROM dbo.STOCK_MOVEMENTS WHERE movement_id = ?", (movement_id,))
        self.commit()
        return cursor.rowcount > 0