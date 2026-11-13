from typing import List, Any


def print_header(title: str, width: int = 60):
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_menu(paragraphs: List[str], title: str = "Menu"):
    print_header(title)
    for i, item in enumerate(paragraphs, 1):
        print(f"  {i}. {item}")
    print("  0. back")
    print("-" * 60)


def print_table(headers: List[str], rows: List[List[Any]]):

    if not rows:
        print("no data")
        return
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    sep_ = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    
    print(sep_)
    header_row = "|" + "|".join(
        f" {str(h).ljust(col_widths[i])} " for i, h in enumerate(headers)
    ) + "|"
    print(header_row)
    print(sep_)
    
    for row in rows:
        data_row = "|" + "|".join(
            f" {str(cell).ljust(col_widths[i])} " for i, cell in enumerate(row)
        ) + "|"
        print(data_row)
    print(sep_)


def input_int(query: str, min_val: int = None, max_val: int = None) -> int:
    while True:
        try:
            value = int(input(query))
            if min_val is not None and value < min_val:
                print(f"Value must be >= {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"Value must be <= {max_val}")
                continue
            return value
        except ValueError:
            print("Input integer num")


def input_str(query: str, allow_empty: bool = False) -> str:
    while True:
        value = input(query).strip()
        if not value and not allow_empty:
            print("Value cant be empty")
            continue
        return value


def input_date(query: str) -> str:
    while True:
        value = input(query).strip()
        try:
            from datetime import datetime
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Incorrect format")