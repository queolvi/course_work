from abc import ABC, abstractmethod
from typing import List

from app.models.batch import Batch


class ReservationStrategy(ABC):
    @abstractmethod
    def select_batches(self, product_id: int, quantity: int) -> List[Batch]:
        pass
    @abstractmethod
    def get_name(self) -> str:
        pass