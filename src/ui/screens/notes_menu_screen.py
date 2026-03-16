from __future__ import annotations

from src.ui.commands.base_command import ActionCommand, BackCommand
from src.ui.screens.menu_screen import MenuScreen


class NotesMenuScreen(MenuScreen):
    title = "NOTES"

    def get_commands(self):
        return [
            ActionCommand("1", "Add note", "Create a new note", self.add_note_screen),
            ActionCommand(
                "2", "Show all notes", "Display all notes", self.show_all_notes_screen
            ),
            ActionCommand(
                "3", "Search notes", "Search by note or tag", self.search_notes_screen
            ),
            ActionCommand(
                "4",
                "Show all tags",
                "Display all unique tags",
                self.show_all_tags_screen,
            ),
            ActionCommand(
                "5", "Edit note", "Edit note by index", self.edit_note_screen
            ),
            ActionCommand(
                "6", "Delete note", "Delete note by index", self.delete_note_screen
            ),
            ActionCommand(
                "7",
                "Delete notes by tag",
                "Delete all notes with a specific tag",
                self.delete_notes_by_tag_screen,
            ),
            BackCommand("0"),
        ]

    def add_note_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("ADD NOTE")

        note = self.input_handler.ask("Enter note (required)")
        tag = self.input_handler.ask("Enter tag (required)")

        result = self.context.notes_service.add_note(note, tag)
        self.printer.print_message(result)
        self.input_handler.pause()

    def show_all_notes_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("ALL NOTES")

        notes = self.context.notes_service.get_all_notes()
        rows = [[str(index), note.note, note.tag or "-"] for index, note in notes]

        self.printer.print_table(["#", "Note", "Tag"], rows)
        self.input_handler.pause()

    def search_notes_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("SEARCH NOTES")

        query = self.input_handler.ask("Search by text or tag")
        notes = self.context.notes_service.search_notes(query)
        rows = [[str(index), note.note, note.tag or "-"] for index, note in notes]

        self.printer.print_table(["#", "Note", "Tag"], rows)
        self.input_handler.pause()

    def delete_note_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("DELETE NOTE")

        index_str = self.input_handler.ask("Enter note index")
        result = self.context.notes_service.delete_note(int(index_str))

        self.printer.print_message(result)
        self.input_handler.pause()

    def delete_notes_by_tag_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("DELETE NOTES BY TAG")

        tag = self.input_handler.ask("Enter tag")
        confirm = self.input_handler.ask(f"Delete '{tag}'? (y/n)").lower()

        if confirm != "y":
            self.printer.print_message("Deletion canceled.")
            self.input_handler.pause()
            return
        result = self.context.notes_service.delete_notes_by_tag(tag)

        self.printer.print_message(result)
        self.input_handler.pause()

    def show_all_tags_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("ALL TAGS")

        tags = self.context.notes_service.get_all_tags()
        rows = [[str(index), tag] for index, tag in enumerate(tags, start=1)]

        self.printer.print_table(["#", "Tag"], rows)
        self.input_handler.pause()

    def edit_note_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("EDIT NOTE")

        index_str = self.input_handler.ask("Enter note index")
        if not index_str.isdigit():
            self.printer.print_message("Invalid index. Please enter a number.")
            self.input_handler.pause()
            return
        new_note = self.input_handler.ask("Enter new note")
        new_tag = self.input_handler.ask("Enter new tag")

        result = self.context.notes_service.edit_note(index_str, new_note, new_tag)
        self.printer.print_message(result)
        self.input_handler.pause()
