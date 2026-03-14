from __future__ import annotations

from src.app.context import AppContext
from src.ui.console.input_handler import InputHandler
from src.ui.console.printer import Printer
from src.ui.screens.main_menu_screen import MainMenuScreen


class Application:
    def __init__(self, context: AppContext) -> None:
        self.context = context
        self.printer = Printer()
        self.input_handler = InputHandler()

    def run(self) -> None:
        main_screen = MainMenuScreen(
            context=self.context,
            printer=self.printer,
            input_handler=self.input_handler,
        )

        try:
            should_continue = main_screen.show()
            if not should_continue:
                print("\nGood bye!")
        except (EOFError, KeyboardInterrupt):
            print("\nGood bye!")
