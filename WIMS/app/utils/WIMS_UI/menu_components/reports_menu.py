from app.utils.WIMS_UI.menu_components.base_menu import BaseMenu
from app.repositories import StockMovementRepository
from app.utils.console_print import print_menu, print_table, input_int, input_str


class ReportsMenu(BaseMenu):
    def run(self):
        repo = StockMovementRepository()
        while True:
            self._clear()
            print_menu([
                "Stock movements (last 20)",
                "Movements by type",
                "Movements by batch",
            ], "Reports")

            choice = input_int("Choose option: ", min_val=0, max_val=3)
            if choice == 0:
                return

            match choice:
                case 1:
                    self._view_all_movements(repo)
                case 2:
                    self._view_by_type(repo)
                case 3:
                    self._view_by_batch(repo)

            self._pause()

    def _view_all_movements(self, repo: StockMovementRepository):
        movements = repo.get_all()[:20]
        if movements:
            rows = [[m.movement_id, m.batch_id, m.type, m.quantity, m.user_id, m.created_at] for m in movements]
            print_table(["ID", "Batch", "Type", "Qty", "User", "Date"], rows)
        else:
            print("\nNo movements found.")

    def _view_by_type(self, repo: StockMovementRepository):
        mtype = input_str("Type: receipt/shipment/write_off/adjustment ")
        movements = repo.get_by_type(mtype)
        if movements:
            rows = [[m.movement_id, m.batch_id, m.quantity, m.user_id, m.created_at] for m in movements]
            print_table(["ID", "Batch", "Qty", "User", "Date"], rows)
        else:
            print("\nNo movements of this type")

    def _view_by_batch(self, repo: StockMovementRepository):
        bid = input_int("Batch ID: ", min_val=1)
        movements = repo.get_by_batch(bid)
        if movements:
            rows = [[m.movement_id, m.type, m.quantity, m.user_id, m.created_at] for m in movements]
            print_table(["ID", "Type", "Qty", "User", "Date"], rows)
        else:
            print("\nNo movements for this batch")