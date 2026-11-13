from abc import ABC, abstractmethod
from datetime import timedelta

from app.models.batch import Batch
from app.models.user import User

class ReservationPolicy(ABC):
    @abstractmethod
    def validate(self, quantity: int, user: User) -> bool:
        pass

    @abstractmethod
    def get_max_reservation_duration(self) -> timedelta:
        pass

    @abstractmethod
    def get_max_quantity_per_user(self) -> int:
        pass

    @abstractmethod
    def can_extend(self, batch: Batch) -> bool:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


class WriteOffPolicy(ABC):
    @abstractmethod
    def can_write_off(self, batch: Batch) -> bool:
        pass

    @abstractmethod
    def get_write_off_reason(self, batch: Batch) -> str:
        pass
    @abstractmethod
    def get_name(self) -> str:
        pass