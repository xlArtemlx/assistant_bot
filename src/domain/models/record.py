from __future__ import annotations

from src.domain.models.fields import Address, Birthday, Email, Name, Phone


class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.address: Address | None = None
        self.phones: list[Phone] = []
        self.email: Email | None = None
        self.birthday: Birthday | None = None

    def rename(self, new_name: str) -> None:
        self.name = Name(new_name)

    def set_address(self, address: str) -> None:
        self.address = Address(address)

    def add_phone(self, phone: str) -> None:
        normalized_phone = Phone(phone).value

        if any(existing.value == normalized_phone for existing in self.phones):
            raise ValueError("This phone already exists.")

        self.phones.append(Phone(normalized_phone))

    def remove_phone(self, phone: str) -> None:
        existing = self.find_phone(phone)
        if existing is None:
            raise ValueError("Phone not found.")

        self.phones.remove(existing)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        existing = self.find_phone(old_phone)
        if existing is None:
            raise ValueError("Phone not found.")

        normalized_new_phone = Phone(new_phone).value

        if any(
            phone.value == normalized_new_phone and phone is not existing
            for phone in self.phones
        ):
            raise ValueError("This phone already exists.")

        existing.value = normalized_new_phone

    def find_phone(self, phone: str) -> Phone | None:
        normalized_phone = phone.strip()

        for item in self.phones:
            if item.value == normalized_phone:
                return item

        return None

    def set_email(self, email: str) -> None:
        self.email = Email(email)

    def add_birthday(self, birthday_str: str) -> None:
        self.birthday = Birthday(birthday_str)

    def address_as_string(self) -> str:
        return self.address.value if self.address else "-"

    def phones_as_string(self) -> str:
        if not self.phones:
            return "-"
        return ", ".join(phone.value for phone in self.phones)

    def email_as_string(self) -> str:
        return self.email.value if self.email else "-"

    def birthday_as_string(self) -> str:
        return str(self.birthday) if self.birthday else "-"

    def __str__(self) -> str:
        return (
            f"Name: {self.name.value}, "
            f"Address: {self.address_as_string()}, "
            f"Phones: {self.phones_as_string()}, "
            f"Email: {self.email_as_string()}, "
            f"Birthday: {self.birthday_as_string()}"
        )