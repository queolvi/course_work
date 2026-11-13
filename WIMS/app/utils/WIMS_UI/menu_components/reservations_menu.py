from pydantic import ValidationError

from app.utils.WIMS_UI.menu_components.base_menu import BaseMenu
from app.repositories import ReservationRepository
from app.schemas import ReservationCreate
from app.logic.reservation_service import ReservationService
from app.utils.console_print import print_header, print_menu, print_table, input_int


class ReservationsMenu(BaseMenu):
    def run(self):
        while True:
            self._clear()
            print_header("Reservations Management")
            print(self._status_line())
            print()
            print_menu([
                "View all reservations",
                "Create reservation (using current strategy + policy)",
                "Cancel expired reservations",
                "View active reservations by current user",
            ], "Reservations")

            choice = input_int("Choose option: ", min_val=0, max_val=4)
            if choice == 0:
                return

            match choice:
                case 1:
                    self._view_reservations()
                case 2:
                    self._create_reservation()
                case 3:
                    self._cancel_expired()
                case 4:
                    self._view_user_reservations()

            self._pause()

    def _status_line(self) -> str:
        user = self.app.current_user.full_name if self.app.current_user else "NOT SELECTED"
        return f"User: {user} | Strategy: {self.app.strategy.get_name()} | Policy: {self.app.policy.get_name()}"

    def _view_reservations(self):
        reservations = ReservationRepository().get_all()
        if reservations:
            rows = [[r.reservation_id, r.batch_id, r.user_id, r.quantity,
                     r.status, r.expires_at.strftime("%Y-%m-%d %H:%M") if r.expires_at else "-"]
                    for r in reservations]
            print_table(["ID", "Batch", "User", "Qty", "Status", "Expires"], rows)
        else:
            print("\nNo reservations found.")

    def _create_reservation(self):
        if not self.app.current_user:
            print("\nPlease select a user first (option 6 in main menu).")
            return

        try:
            product_id = input_int("Product ID: ", min_val=1)
            quantity = input_int("Quantity: ", min_val=1)
            duration_hours = input_int("Duration (hours, 1-168): ", min_val=1, max_val=168)

            data = {
                "batch_id": 0,
                "user_id": self.app.current_user.user_id,
                "quantity": quantity,
                "duration_hours": duration_hours,
            }
            res_data = ReservationCreate(**data)

            service = ReservationService(self.app.strategy, self.app.policy)
            reservations = service.create_reservation(
                product_id=product_id,
                quantity=res_data.quantity,
                user=self.app.current_user,
            )

            print(f"\nCreated {len(reservations)} reservation(s):")
            for r in reservations:
                print(f"Reservation #{r.reservation_id}: batch={r.batch_id}, qty={r.quantity}, expires={r.expires_at}")

        except ValidationError as e:
            self._print_validation_error(e)
        except ValueError as e:
            print(f"\n{e}")
        except Exception as e:
            print(f"\n{e}")

    def _cancel_expired(self):
        service = ReservationService(self.app.strategy, self.app.policy)
        count = service.cancel_expired_reservations()
        print(f"\nCancelled {count} expired reservations")

    def _view_user_reservations(self):
        if not self.app.current_user:
            print("\nPlease select a user first")
            return

        reservations = ReservationRepository().get_active_by_user(self.app.current_user.user_id)
        if reservations:
            rows = [[r.reservation_id, r.batch_id, r.quantity, r.status, r.expires_at] for r in reservations]
            print_table(["ID", "Batch", "Qty", "Status", "Expires"], rows)
        else:
            print("\nNo active reservations for this user")