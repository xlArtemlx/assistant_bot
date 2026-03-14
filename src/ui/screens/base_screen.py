from __future__ import annotations

from abc import ABC, abstractmethod

from src.app.context import AppContext
from src.ui.console.input_handler import InputHandler
from src.ui.console.printer import Printer


class Screen(ABC):
    def __init__(
        self,
        context: AppContext,
        printer: Printer,
        input_handler: InputHandler,
    ) -> None:
        self.context = context
        self.printer = printer
        self.input_handler = input_handler

    @abstractmethod
    def show(self) -> bool:
        raise NotImplementedError
