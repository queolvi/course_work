from datetime import datetime
from typing import List

from app.models.batch import Batch
from app.models.user import User
from app.models.reservation import Reservation, reservations_statuses
from app.repositories.batch_repo import BatchRepository
from app.repositories.reservation_repo import ReservationRepository
from app.logic.strategies.base_strategy import ReservationStrategy
from app.logic.policies.base_policy import ReservationPolicy


class ReservationService:

    def __init__(self, strategy: ReservationStrategy, policy: ReservationPolicy):
        self.strategy = strategy
        self.policy = policy
        self.batch_repo = BatchRepository()
        self.reservation_repo = ReservationRepository()

    def create_reservation(
        self, product_id: int, quantity: int, user: User
    ) -> List[Reservation]:

        if not self.policy.validate(quantity, user):
            raise ValueError(
                f"Reservation policy violated: quantity {quantity} exceeds "
                f"max {self.policy.get_max_quantity_per_user()} per user"
            )

        selected_batches = self.strategy.select_batches(product_id, quantity)
        
        if not selected_batches:
            raise ValueError(
                f"Insufficient stock for product_id={product_id}, quantity={quantity}"
            )

        created_reservations = []
        expires_at = datetime.now() + self.policy.get_max_reservation_duration()

        for batch in selected_batches:
            reserve_qty = getattr(batch, "_reserve_quantity", batch.available_quantity)
            reservation_id = self.reservation_repo.create(
                batch_id=batch.batch_id,
                user_id=user.user_id,
                quantity=reserve_qty,
                expires_at=expires_at,
            )

            self.batch_repo.increase_reserved(batch.batch_id, reserve_qty)
            reservation = self.reservation_repo.get_by_id(reservation_id)

            if reservation:
                created_reservations.append(reservation)

        return created_reservations

    def cancel_expired_reservations(self) -> int:
        
        expired_reservations = self.reservation_repo.get_expired_active()
        cancelled_count = 0

        for reservation in expired_reservations:
            self.batch_repo.decrease_reserved(reservation.batch_id, reservation.quantity)
            self.reservation_repo.update_status(
                reservation.reservation_id, reservations_statuses.cancelled.value
            )
            cancelled_count += 1
        
        return cancelled_count

    def get_strategy_name(self) -> str:
        return self.strategy.get_name()

    def get_policy_name(self) -> str:
        return self.policy.get_name()