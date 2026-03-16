from __future__ import annotations

from src.data.repositories.address_book_repository import AddressBookRepository
from src.domain.models.address_book import AddressBook
from src.domain.models.record import Record
from src.utils.decorators import input_error


class ContactService:
    def __init__(
        self,
        book: AddressBook,
        repository: AddressBookRepository,
    ) -> None:
        self._book = book
        self._repository = repository

    def get_record_or_raise(self, name: str) -> Record:
        record = self._book.find(name)
        if record is None:
            raise ValueError("Contact not found.")
        return record

    @input_error
    def add_contact(
        self,
        name: str,
        address: str = "",
        phone: str = "",
        email: str = "",
    ) -> str:
        record = self._book.find(name)

        if record is None:
            record = Record(name)
            self._book.add_record(record)
            message = "Contact added."
            if address.strip():
                record.set_address(address)

            if phone.strip():
                record.add_phone(phone)

            if email.strip():
                record.set_email(email)
        else:
            message = "Contact already exists"

        self._repository.save(self._book)
        return message

    @input_error
    def edit_contact_name(self, old_name: str, new_name: str) -> str:
        record = self.get_record_or_raise(old_name)

        if old_name.strip().lower() == new_name.strip().lower():
            return "Nothing changed."

        if self._book.find(new_name) is not None:
            raise ValueError("A contact with this name already exists.")

        self._book.delete(old_name)
        record.rename(new_name)
        self._book.add_record(record)

        self._repository.save(self._book)
        return "Contact name updated."

    @input_error
    def set_address(self, name: str, address: str) -> str:
        record = self.get_record_or_raise(name)
        record.set_address(address)
        self._repository.save(self._book)
        return "Address saved."

    @input_error
    def add_phone(self, name: str, phone: str) -> str:
        record = self.get_record_or_raise(name)
        record.add_phone(phone)
        self._repository.save(self._book)
        return "Phone added."

    @input_error
    def edit_phone(self, name: str, old_phone: str, new_phone: str) -> str:
        record = self.get_record_or_raise(name)
        record.edit_phone(old_phone, new_phone)
        self._repository.save(self._book)
        return "Phone updated."

    @input_error
    def remove_phone(self, name: str, phone: str) -> str:
        record = self.get_record_or_raise(name)
        record.remove_phone(phone)
        self._repository.save(self._book)
        return "Phone removed."

    @input_error
    def set_email(self, name: str, email: str) -> str:
        record = self.get_record_or_raise(name)
        record.set_email(email)
        self._repository.save(self._book)
        return "Email saved."

    @input_error
    def delete_contact(self, name: str) -> str:
        self._book.delete(name)
        self._repository.save(self._book)
        return "Contact deleted."

    def get_contact_details(self, name: str) -> Record:
        return self.get_record_or_raise(name)

    def get_all_contacts(self) -> list[Record]:
        return self._book.get_all()

    def search_contacts(self, query: str) -> list[Record]:
        return self._book.search(query)
