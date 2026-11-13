from app.models.batch import Batch
from app.models.reservation import reservations_statuses
from app.logic.policies.base_policy import WriteOffPolicy


class AutoWriteOffPolicy(WriteOffPolicy):

    def can_write_off(self, batch: Batch) -> bool:
        if not batch.is_expired:
            return False
        if batch.reserved_quantity > 0:
            return False
        return True

    def get_write_off_reason(self, batch: Batch) -> str:
        return f"Batch expired on {batch.expiration_date} with no active reservations"

    def get_name(self) -> str:
        return "Auto Write-Off Policy"