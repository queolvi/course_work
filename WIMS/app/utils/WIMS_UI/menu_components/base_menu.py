import os
from typing import TYPE_CHECKING

from app.utils.console_print import (
    print_header,
    print_menu,
    print_table,
    input_int,
    input_str,
    input_date,
)

if TYPE_CHECKING:
    from app.application import WIMS_UI


class BaseMenu:
    def __init__(self, app: "WIMS_UI"):
        self.app = app

    def _clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def _pause(self):
        input("\nPress Enter to continue")

    def _print_validation_error(self, e):
        print("\nValidation failed:")
        for err in e.errors():
            field = ".".join(str(loc) for loc in err["loc"])
            print(f"  - {field}: {err['msg']}")

    def run(self):
        raise NotImplementedError