from __future__ import annotations

from src.ui.commands.base_command import Command, CommandResult
from src.ui.screens.base_screen import Screen


class MenuScreen(Screen):
    title: str = ""
    subtitle: str | None = None

    def get_commands(self) -> list[Command]:
        raise NotImplementedError

    def show(self) -> bool:
        while True:
            self.printer.clear_screen()
            self.printer.print_header(self.title, self.subtitle)

            commands = self.get_commands()
            self._render_commands(commands)

            choice = self.input_handler.ask()
            command = self._find_command(commands, choice)

            if command is None:
                self.printer.print_message("Invalid option.")
                self.input_handler.pause()
                continue

            result = command.execute()

            if result == CommandResult.CONTINUE:
                continue

            if result == CommandResult.BACK:
                return True

            if result == CommandResult.EXIT_APP:
                return False

    def _render_commands(self, commands: list[Command]) -> None:
        key_width = max(len(command.key) for command in commands)
        label_width = max(len(command.label) for command in commands)

        for command in commands:
            left = f"{command.key.rjust(key_width)}. {command.label.ljust(label_width)}"
            print(f"{left}  —  {command.description}")

    def _find_command(self, commands: list[Command], choice: str) -> Command | None:
        for command in commands:
            if command.key == choice:
                return command
        return None