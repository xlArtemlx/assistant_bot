from __future__ import annotations

from src.ui.commands.base_command import ExitCommand, OpenScreenCommand
from src.ui.screens.birthdays_menu_screen import BirthdaysMenuScreen
from src.ui.screens.contacts_menu_screen import ContactsMenuScreen
from src.ui.screens.menu_screen import MenuScreen
from src.ui.screens.notes_menu_screen import NotesMenuScreen


class MainMenuScreen(MenuScreen):
    title = "ASSISTANT BOT"
    subtitle = "Personal organizer for contacts, birthdays and notes"

    def get_commands(self):
        return [
            OpenScreenCommand(
                "1",
                "Contacts",
                "Manage contacts",
                lambda: ContactsMenuScreen(self.context, self.printer, self.input_handler),
            ),
            OpenScreenCommand(
                "2",
                "Birthdays",
                "Manage birthdays",
                lambda: BirthdaysMenuScreen(self.context, self.printer, self.input_handler),
            ),
            OpenScreenCommand(
                "3",
                "Notes",
                "Open notes",
                lambda: NotesMenuScreen(self.context, self.printer, self.input_handler),
            ),
            ExitCommand("0"),
        ]