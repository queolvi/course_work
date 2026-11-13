from typing import List

from app.models.batch import Batch
from app.repositories.batch_repo import BatchRepository
from app.logic.strategies.base_strategy import ReservationStrategy


class FEFOReservationStrategy(ReservationStrategy):
    def __init__(self):
        self.batch_repo = BatchRepository()

    def select_batches(self, product_id: int, quantity: int) -> List[Batch]:
        
        batches = self.batch_repo.get_fefo_batches(product_id)
        
        if not batches:
            return []

        selected_batches = []
        remaining_quantity = quantity
        
        for batch in batches:
            if remaining_quantity <= 0:
                break
            
            available = batch.available_quantity
            if available <= 0:
                continue
            
            take_quantity = min(available, remaining_quantity)
            
            batch_copy = Batch(
                batch_id=batch.batch_id,
                product_id=batch.product_id,
                quantity=batch.quantity,
                reserved_quantity=batch.reserved_quantity,
                manufacture_date=batch.manufacture_date,
                expiration_date=batch.expiration_date,
                location_id=batch.location_id,
                created_at=batch.created_at,
            )

            batch_copy._reserve_quantity = take_quantity
            selected_batches.append(batch_copy)
            remaining_quantity -= take_quantity
        if remaining_quantity > 0:
            return []
        
        return selected_batches

    def get_name(self) -> str:
        return "First Expired First Out"