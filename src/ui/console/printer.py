from __future__ import annotations

import os
import shutil
from collections.abc import Iterable


class Printer:
    def clear_screen(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def get_terminal_width(self, default: int = 80) -> int:
        return shutil.get_terminal_size((default, 24)).columns

    def print_header(self, title: str, subtitle: str | None = None) -> None:
        width = min(self.get_terminal_width(), 100)
        inner_width = width - 2

        print("╔" + "═" * inner_width + "╗")
        print("║" + title.center(inner_width) + "║")

        if subtitle:
            print("╟" + "─" * inner_width + "╢")
            print("║" + subtitle.center(inner_width) + "║")

        print("╚" + "═" * inner_width + "╝")

    def print_message(self, message: str) -> None:
        print(f"\n• {message}")

    def print_hint(self, message: str) -> None:
        print(f"\n{message}")

    def print_table(self, headers: list[str], rows: Iterable[list[str]]) -> None:
        materialized_rows = list(rows)

        if not materialized_rows:
            self.print_message("No data.")
            return

        widths = [len(header) for header in headers]

        for row in materialized_rows:
            for index, cell in enumerate(row):
                widths[index] = max(widths[index], len(str(cell)))

        separator = "+-" + "-+-".join("-" * width for width in widths) + "-+"
        header_line = (
            "| "
            + " | ".join(
                headers[index].ljust(widths[index]) for index in range(len(headers))
            )
            + " |"
        )

        print(separator)
        print(header_line)
        print(separator)

        for row in materialized_rows:
            row_line = (
                "| "
                + " | ".join(
                    str(row[index]).ljust(widths[index]) for index in range(len(row))
                )
                + " |"
            )
            print(row_line)

        print(separator)
