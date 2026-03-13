from __future__ import annotations

from datetime import datetime

from src.data.repositories.address_book_repository import AddressBookRepository
from src.domain.models.address_book import AddressBook
from src.utils.decorators import input_error


class BirthdayService:
    def __init__(
        self,
        book: AddressBook,
        repository: AddressBookRepository,
    ) -> None:
        self._book = book
        self._repository = repository

    def _get_record_or_raise(self, name: str):
        record = self._book.find(name)
        if record is None:
            raise ValueError("Contact not found.")
        return record

    @staticmethod
    def _parse_days(days: str | int) -> int:
        if isinstance(days, int):
            parsed_days = days
        else:
            normalized_days = days.strip()

            if not normalized_days:
                raise ValueError("Number of days is required.")

            if not normalized_days.isdigit():
                raise ValueError("Number of days must be a positive integer.")

            parsed_days = int(normalized_days)

        if parsed_days < 0:
            raise ValueError("Number of days cannot be negative.")

        return parsed_days

    @input_error
    def add_or_update_birthday(self, name: str, birthday_str: str) -> str:
        record = self._get_record_or_raise(name)
        record.add_birthday(birthday_str)
        self._repository.save(self._book)
        return "Birthday saved."

    @input_error
    def get_birthday(self, name: str) -> str:
        record = self._get_record_or_raise(name)

        if record.birthday is None:
            return "Birthday not set."

        return str(record.birthday)

    @input_error
    def get_upcoming_birthdays_grouped(
        self,
        days: str | int = 7,
    ) -> list[tuple[str, str]] | str:
        parsed_days = self._parse_days(days)
        upcoming = self._book.get_upcoming_birthdays(days=parsed_days)

        if not upcoming:
            return []

        grouped: dict[str, list[str]] = {}

        for item in upcoming:
            grouped.setdefault(item["congratulation_date"], []).append(item["name"])

        result: list[tuple[str, str]] = []

        for date_str in sorted(
            grouped.keys(),
            key=lambda value: datetime.strptime(value, "%d.%m.%Y").date(),
        ):
            result.append((date_str, ", ".join(grouped[date_str])))

        return result