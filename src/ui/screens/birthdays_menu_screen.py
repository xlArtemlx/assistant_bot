from __future__ import annotations

from src.ui.commands.base_command import ActionCommand, BackCommand
from src.ui.screens.menu_screen import MenuScreen


class BirthdaysMenuScreen(MenuScreen):
    title = "BIRTHDAYS"

    def get_commands(self):
        return [
            ActionCommand("1", "Add or update", "Add or update birthday", self.add_birthday_screen),
            ActionCommand("2", "Show birthday", "Show contact birthday", self.show_birthday_screen),
            ActionCommand("3", "Upcoming birthdays", "Show upcoming birthdays", self.upcoming_birthdays_screen),
            BackCommand("0"),
        ]

    def add_birthday_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("ADD OR UPDATE BIRTHDAY")

        name = self.input_handler.ask("Enter contact name")
        birthday = self.input_handler.ask("Enter birthday (DD.MM.YYYY)")

        result = self.context.birthday_service.add_or_update_birthday(name, birthday)
        self.printer.print_message(result)
        self.input_handler.pause()

    def show_birthday_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("SHOW BIRTHDAY")

        name = self.input_handler.ask("Enter contact name")
        result = self.context.birthday_service.get_birthday(name)

        self.printer.print_message(result)
        self.input_handler.pause()

    def upcoming_birthdays_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("UPCOMING BIRTHDAYS")

        days = self.input_handler.ask("Enter number of days")
        items = self.context.birthday_service.get_upcoming_birthdays_grouped(days)

        if isinstance(items, str):
            self.printer.print_message(items)
            self.input_handler.pause()
            return

        rows = [[date_str, names] for date_str, names in items]
        self.printer.print_table(["Congratulation date", "Contacts"], rows)
        self.input_handler.pause()