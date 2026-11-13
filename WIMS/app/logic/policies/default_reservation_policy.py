from datetime import timedelta

from app.models.batch import Batch
from app.models.user import User
from app.logic.policies.base_policy import ReservationPolicy


class DefaultReservationPolicy(ReservationPolicy):
    def __init__(self):
        self._max_duration = timedelta(hours=24)
        self._max_quantity_per_user = 100

    def validate(self, quantity: int, user: User) -> bool:
        if quantity <= 0:
            return False
        if quantity > self._max_quantity_per_user:
            return False
        return True

    def get_max_reservation_duration(self) -> timedelta:
        return self._max_duration

    def get_max_quantity_per_user(self) -> int:
        return self._max_quantity_per_user

    def can_extend(self, batch: Batch) -> bool:
        return batch.available_quantity > 0

    def get_name(self) -> str:
        return "Default Reservation Policy, 24 hours and 100 units"