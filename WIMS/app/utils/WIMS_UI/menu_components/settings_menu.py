from app.utils.WIMS_UI.menu_components.base_menu import BaseMenu
from app.logic.strategies import FEFOReservationStrategy, FIFOReservationStrategy, LIFOReservationStrategy
from app.logic.policies import DefaultReservationPolicy, VIPReservationPolicy
from app.utils.console_print import print_header, print_menu, input_int


class SettingsMenu(BaseMenu):
    def run(self):
        while True:
            self._clear()
            print_header("Settings — Strategy & Policy")
            print(f"Current strategy: {self.app.strategy.get_name()}")
            print(f"Current policy:   {self.app.policy.get_name()}")
            print()
            print_menu([
                "Change reservation strategy",
                "Change reservation policy",
            ], "Settings")

            choice = input_int("Choose option: ", min_val=0, max_val=2)
            if choice == 0:
                return

            match choice:
                case 1:
                    self._change_strategy()
                case 2:
                    self._change_policy()

            self._pause()

    def _change_strategy(self):
        print("\n  1. FEFO (First Expired, First Out)")
        print("  2. FIFO (First In, First Out)")
        print("  3. LIFO (Last In, First Out)")
        s = input_int("Select (1-3): ", min_val=1, max_val=3)
        self.app.strategy = [FEFOReservationStrategy(), FIFOReservationStrategy(), LIFOReservationStrategy()][s - 1]
        print(f"[OK] Strategy: {self.app.strategy.get_name()}")

    def _change_policy(self):
        print("\n1. Default = 24h and max 100 units)")
        print("2. VIP = 72h and max 1000 units)")
        p = input_int("Select: ", min_val=1, max_val=2)
        self.app.policy = [DefaultReservationPolicy(), VIPReservationPolicy()][p - 1]
        print(f"Policy: {self.app.policy.get_name()}")