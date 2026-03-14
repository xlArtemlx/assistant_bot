from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from enum import Enum, auto


class CommandResult(Enum):
    CONTINUE = auto()
    BACK = auto()
    EXIT_APP = auto()


class Command(ABC):
    @property
    @abstractmethod
    def key(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def label(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def execute(self) -> CommandResult:
        raise NotImplementedError


class ActionCommand(Command):
    def __init__(
        self,
        key: str,
        label: str,
        description: str,
        handler: Callable[[], None],
    ) -> None:
        self._key = key
        self._label = label
        self._description = description
        self._handler = handler

    @property
    def key(self) -> str:
        return self._key

    @property
    def label(self) -> str:
        return self._label

    @property
    def description(self) -> str:
        return self._description

    def execute(self) -> CommandResult:
        self._handler()
        return CommandResult.CONTINUE


class OpenScreenCommand(Command):
    def __init__(
        self,
        key: str,
        label: str,
        description: str,
        screen_factory: Callable[[], object],
    ) -> None:
        self._key = key
        self._label = label
        self._description = description
        self._screen_factory = screen_factory

    @property
    def key(self) -> str:
        return self._key

    @property
    def label(self) -> str:
        return self._label

    @property
    def description(self) -> str:
        return self._description

    def execute(self) -> CommandResult:
        screen = self._screen_factory()
        should_continue = screen.show()

        if should_continue:
            return CommandResult.CONTINUE

        return CommandResult.EXIT_APP


class BackCommand(Command):
    def __init__(self, key: str = "0") -> None:
        self._key = key

    @property
    def key(self) -> str:
        return self._key

    @property
    def label(self) -> str:
        return "Back"

    @property
    def description(self) -> str:
        return "Return to previous menu"

    def execute(self) -> CommandResult:
        return CommandResult.BACK


class ExitCommand(Command):
    def __init__(self, key: str = "0") -> None:
        self._key = key

    @property
    def key(self) -> str:
        return self._key

    @property
    def label(self) -> str:
        return "Exit"

    @property
    def description(self) -> str:
        return "Close application"

    def execute(self) -> CommandResult:
        return CommandResult.EXIT_APP
