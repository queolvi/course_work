from datetime import datetime
from typing import List, Optional

from app.models.reservation import reservations_statuses
from app.models.reservation import Reservation

from app.repositories.base_repo import BaseRepository


class ReservationRepository(BaseRepository[Reservation]):

    def _map_row(self, row) -> Reservation:
        return Reservation(
            reservation_id=row.reservation_id,
            batch_id=row.batch_id,
            user_id=row.user_id,
            quantity=row.quantity,
            status=row.status,
            expires_at=row.expires_at,
            order_id=row.order_id,
            created_at=row.created_at,)

    def get_all(self) -> List[Reservation]:
        return self._fetch_all(
            "SELECT reservation_id, batch_id, user_id, quantity, status, "
            "expires_at, order_id, created_at FROM dbo.RESERVATIONS")

    def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        return self._fetch_one(
            "SELECT reservation_id, batch_id, user_id, quantity, status, "
            "expires_at, order_id, created_at FROM dbo.RESERVATIONS WHERE reservation_id = ?",
            (reservation_id,),)

    def get_active_by_batch(self, batch_id: int) -> List[Reservation]:
        return self._fetch_all(
            "SELECT reservation_id, batch_id, user_id, quantity, status, "
            "expires_at, order_id, created_at FROM dbo.RESERVATIONS "
            "WHERE batch_id = ? AND status = N'active'",
            (batch_id,), )

    def get_active_by_user(self, user_id: int) -> List[Reservation]:
        return self._fetch_all(
            "SELECT reservation_id, batch_id, user_id, quantity, status, "
            "expires_at, order_id, created_at FROM dbo.RESERVATIONS "
            "WHERE user_id = ? AND status = N'active'",
            (user_id,),)

    def get_expired_active(self) -> List[Reservation]:
        return self._fetch_all(
            "SELECT reservation_id, batch_id, user_id, quantity, status, "
            "expires_at, order_id, created_at FROM dbo.RESERVATIONS "
            "WHERE status = N'active' AND expires_at < GETDATE()",)

    def create(
        self,
        batch_id: int,
        user_id: int,
        quantity: int,
        expires_at: datetime,
        order_id: Optional[int] = None,) -> int:
        cursor = self._execute(
            "INSERT INTO dbo.RESERVATIONS "
            "(batch_id, user_id, order_id, quantity, expires_at) "
            "OUTPUT INSERTED.reservation_id VALUES (?, ?, ?, ?, ?)",
            (batch_id, user_id, order_id, quantity, expires_at),)
        self.commit()
        return cursor.fetchone().reservation_id

    def update_status(self, reservation_id: int, status: reservations_statuses) -> bool:
        cursor = self._execute(
            "UPDATE dbo.RESERVATIONS SET status = ? WHERE reservation_id = ?",
            (status, reservation_id),)
        self.commit()
        return cursor.rowcount > 0

    def cancel_expired_reservations(self) -> int:
        cursor = self._execute(
            "UPDATE dbo.RESERVATIONS SET status = N'cancelled' "
            "WHERE status = N'active' AND expires_at < GETDATE()")
        self.commit()
        return cursor.rowcount

    def delete(self, reservation_id: int) -> bool:
        cursor = self._execute(
            "DELETE FROM dbo.RESERVATIONS WHERE reservation_id = ?", (reservation_id,))
        self.commit()
        return cursor.rowcount > 0