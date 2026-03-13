from __future__ import annotations

from src.domain.models.record import Record
from src.ui.commands.base_command import ActionCommand, BackCommand
from src.ui.screens.menu_screen import MenuScreen


class ContactsMenuScreen(MenuScreen):
    title = "CONTACTS"

    def get_commands(self):
        return [
            ActionCommand("1", "Add contact", "Create or update contact", self.add_contact_screen),
            ActionCommand("2", "Edit contact name", "Edit contact name", self.edit_contact_name_screen),
            ActionCommand("3", "Set address", "Set address for contact", self.set_address_screen),
            ActionCommand("4", "Add phone", "Add phone to contact", self.add_phone_screen),
            ActionCommand("5", "Edit phone", "Edit phone of contact", self.edit_phone_screen),
            ActionCommand("6", "Remove phone", "Remove phone from contact", self.remove_phone_screen),
            ActionCommand("7", "Set email", "Set email for contact", self.set_email_screen),
            ActionCommand("8", "Show all contacts", "Display all contacts", self.show_all_contacts_screen),
            ActionCommand("9", "Search contact", "Search for a contact", self.search_contacts_screen),
            ActionCommand("10", "View contact details", "View details of a contact", self.view_contact_screen),
            ActionCommand("11", "Delete contact", "Delete a contact", self.delete_contact_screen),
            BackCommand("0"),
        ]

    def add_contact_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("ADD CONTACT")

        name = self.input_handler.ask("Enter name")
        address = self.input_handler.ask("Enter address (optional)")
        phone = self.input_handler.ask("Enter phone (optional, 10 digits)")
        email = self.input_handler.ask("Enter email (optional)")

        result = self.context.contact_service.add_contact(name, address, phone, email)
        self.printer.print_message(result)
        self.input_handler.pause()

    def edit_contact_name_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("EDIT CONTACT NAME")

        old_name = self.input_handler.ask("Enter current name")
        new_name = self.input_handler.ask("Enter new name")

        result = self.context.contact_service.edit_contact_name(old_name, new_name)
        self.printer.print_message(result)
        self.input_handler.pause()

    def set_address_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("SET ADDRESS")

        name = self.input_handler.ask("Enter contact name")
        address = self.input_handler.ask("Enter address")

        result = self.context.contact_service.set_address(name, address)
        self.printer.print_message(result)
        self.input_handler.pause()

    def add_phone_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("ADD PHONE")

        name = self.input_handler.ask("Enter contact name")
        phone = self.input_handler.ask("Enter new phone")

        result = self.context.contact_service.add_phone(name, phone)
        self.printer.print_message(result)
        self.input_handler.pause()

    def edit_phone_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("EDIT PHONE")

        name = self.input_handler.ask("Enter contact name")
        old_phone = self.input_handler.ask("Enter current phone")
        new_phone = self.input_handler.ask("Enter new phone")

        result = self.context.contact_service.edit_phone(name, old_phone, new_phone)
        self.printer.print_message(result)
        self.input_handler.pause()

    def remove_phone_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("REMOVE PHONE")

        name = self.input_handler.ask("Enter contact name")
        phone = self.input_handler.ask("Enter phone to remove")

        result = self.context.contact_service.remove_phone(name, phone)
        self.printer.print_message(result)
        self.input_handler.pause()

    def set_email_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("SET EMAIL")

        name = self.input_handler.ask("Enter contact name")
        email = self.input_handler.ask("Enter email")

        result = self.context.contact_service.set_email(name, email)
        self.printer.print_message(result)
        self.input_handler.pause()

    def show_all_contacts_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("ALL CONTACTS")

        contacts = self.context.contact_service.get_all_contacts()
        rows = [self._record_to_row(record) for record in contacts]

        self.printer.print_table(["Name", "Address", "Phones", "Email", "Birthday"], rows)
        self.input_handler.pause()

    def search_contacts_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("SEARCH CONTACTS")

        query = self.input_handler.ask("Search by name, phone or email")
        results = self.context.contact_service.search_contacts(query)
        rows = [self._record_to_row(record) for record in results]

        self.printer.print_table(["Name", "Address", "Phones", "Email", "Birthday"], rows)
        self.input_handler.pause()

    def view_contact_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("VIEW CONTACT DETAILS")

        try:
            name = self.input_handler.ask("Enter contact name")
            record = self.context.contact_service.get_contact_details(name)

            rows = [
                ["Name", record.name.value],
                ["Address", record.address_as_string()],
                ["Phones", record.phones_as_string()],
                ["Email", record.email_as_string()],
                ["Birthday", record.birthday_as_string()],
            ]

            self.printer.print_table(["Field", "Value"], rows)
        except Exception as error:
            self.printer.print_message(str(error))

        self.input_handler.pause()

    def delete_contact_screen(self) -> None:
        self.printer.clear_screen()
        self.printer.print_header("DELETE CONTACT")

        name = self.input_handler.ask("Enter contact name")
        confirm = self.input_handler.ask(f"Delete '{name}'? (y/n)").lower()

        if confirm != "y":
            self.printer.print_message("Deletion canceled.")
            self.input_handler.pause()
            return

        result = self.context.contact_service.delete_contact(name)
        self.printer.print_message(result)
        self.input_handler.pause()

    @staticmethod
    def _record_to_row(record: Record) -> list[str]:
        return [
            record.name.value,
            record.address_as_string(),
            record.phones_as_string(),
            record.email_as_string(),
            record.birthday_as_string(),
        ]