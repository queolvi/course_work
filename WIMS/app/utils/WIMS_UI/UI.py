import os

from app.core.database import db
from app.models.user import User
from app.repositories import UserRepository
from app.utils.console_print import print_header, print_menu, print_table, input_int
from app.utils.WIMS_UI.menu_components import (
    ProductsMenu,
    BatchesMenu,
    ReservationsMenu,
    ReportsMenu,
    SettingsMenu,
)


class WIMS_Interface:
    def __init__(self):
        from app.logic.strategies import FEFOReservationStrategy
        from app.logic.policies import DefaultReservationPolicy
        
        self.strategy = FEFOReservationStrategy()
        self.policy = DefaultReservationPolicy()
        self.current_user: User | None = None
        self._running = False

        self.products_menu = ProductsMenu(self)
        self.batches_menu = BatchesMenu(self)
        self.reservations_menu = ReservationsMenu(self)
        self.reports_menu = ReportsMenu(self)
        self.settings_menu = SettingsMenu(self)

    def _clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def _pause(self):
        input("\nPress Enter to continue")

    def _status_line(self) -> str:
        user = self.app.current_user.full_name if self.current_user else "NOT SELECTED"
        return f"User: {user} | Strategy: {self.strategy.get_name()} | Policy: {self.policy.get_name()}"

    def _select_user(self) -> User | None:
        users = UserRepository().get_all()
        if not users:
            print("\nNo users found")
            return None

        print_header("Select current user")
        rows = [[u.user_id, u.username, u.full_name, u.role_id] for u in users]
        print_table(["ID", "Username", "Full Name", "Role ID"], rows)

        user_id = input_int("Enter user ID, if 0, then cancel ", min_val=0)
        if user_id == 0:
            return None

        user = UserRepository().get_by_id(user_id)
        if not user:
            print("User not found.")
            return None

        print(f"Logged in as: {user.full_name}")
        return user

    def run(self):
        print_header("Start")
        try:
            db.connect()
            print("connection with db")
        except Exception as e:
            print(f"Cannot connect to database: {e}")
            print("Please check .env and MSSQL is running.")
            return

        self._running = True
        try:
            self._main_loop()
        except KeyboardInterrupt:
            print("\n\nInterrupted by user.")
        finally:
            db.close()

    def _main_loop(self):
        while self._running:
            self._clear()
            print_header("")
            print(self._status_line())
            print()
            print_menu([
                "Products management",
                "Batches management",
                "Reservations management",
                "Reports",
                "Settings (strategy & policy)",
                "Select / change user",
                "Exit",
            ], "Main Menu")

            choice = input_int("Choose option: ", min_val=0, max_val=7)

            match choice:
                case 0 | 7:
                    print("\nExit")
                    self._running = False
                case 1:
                    self.products_menu.run()
                case 2:
                    self.batches_menu.run()
                case 3:
                    self.reservations_menu.run()
                case 4:
                    self.reports_menu.run()
                case 5:
                    self.settings_menu.run()
                case 6:
                    self.current_user = self._select_user()
                    self._pause()