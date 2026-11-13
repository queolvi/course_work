from pydantic import ValidationError

from app.utils.WIMS_UI.menu_components.base_menu import BaseMenu
from app.repositories import BatchRepository
from app.schemas import BatchCreate
from app.utils.console_print import print_menu, print_table, input_int, input_date


class BatchesMenu(BaseMenu):
    def run(self):
        repo = BatchRepository()
        while True:
            self._clear()
            print_menu([
                "View all batches",
                "Create new batch",
                "View expired batches",
                "View batches expiring soon (7 days)",
                "Delete batch",
            ], "Batches Management")

            choice = input_int("Choose option: ", min_val=0, max_val=5)
            if choice == 0:
                return

            match choice:
                case 1:
                    self._view_batches(repo)
                case 2:
                    self._create_batch(repo)
                case 3:
                    self._view_expired(repo)
                case 4:
                    self._view_expiring_soon(repo)
                case 5:
                    self._delete_batch(repo)

            self._pause()

    def _view_batches(self, repo: BatchRepository):
        batches = repo.get_all()
        if batches:
            rows = [[b.batch_id, b.product_id, b.quantity, b.reserved_quantity,
                     b.available_quantity, b.expiration_date] for b in batches]
            print_table(["ID", "Prod", "Qty", "Res", "Avail", "Expires"], rows)
        else:
            print("\nNo batches found.")

    def _create_batch(self, repo: BatchRepository):
        try:
            data = {
                "product_id": input_int("Product ID: ", min_val=1),
                "quantity": input_int("Quantity: ", min_val=1),
                "manufacture_date": input_date("Manufacture date (YYYY-MM-DD): "),
                "expiration_date": input_date("Expiration date (YYYY-MM-DD): "),
                "location_id": input_int("Location ID: ", min_val=1),
            }
            batch_data = BatchCreate(**data)
            bid = repo.create(
                product_id=batch_data.product_id,
                quantity=batch_data.quantity,
                manufacture_date=batch_data.manufacture_date,
                expiration_date=batch_data.expiration_date,
                location_id=batch_data.location_id,
            )
            print(f"\nBatch created with id={bid}")
        except ValidationError as e:
            self._print_validation_error(e)
        except Exception as e:
            print(f"\n{e}")

    def _view_expired(self, repo: BatchRepository):
        expired = repo.get_expired_batches()
        if expired:
            rows = [[b.batch_id, b.product_id, b.quantity, b.expiration_date, b.days_until_expiration] for b in expired]
            print_table(["ID", "Prod", "Qty", "Expires", "Days ago"], rows)
        else:
            print("\n  No expired batches.")

    def _view_expiring_soon(self, repo: BatchRepository):
        soon = repo.get_expiring_soon(days=7)
        if soon:
            rows = [[b.batch_id, b.product_id, b.quantity, b.expiration_date, b.days_until_expiration] for b in soon]
            print_table(["ID", "Prod", "Qty", "Expires", "Days left"], rows)
        else:
            print("\n  No batches expiring in 7 days.")

    def _delete_batch(self, repo: BatchRepository):
        bid = input_int("Batch ID to delete: ", min_val=1)
        if repo.delete(bid):
            print("Batch deleted.")
        else:
            print("Cannot delete.")