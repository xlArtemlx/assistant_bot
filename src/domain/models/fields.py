from __future__ import annotations

from datetime import date, datetime
import re


class Field:
    def __init__(self, value: str) -> None:
        self.value = value

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._value = self._normalize(value)

    def _normalize(self, value: str) -> str:
        return value

    def __str__(self) -> str:
        return self.value


class Name(Field):
    def _normalize(self, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Name is required.")
        return normalized


class Phone(Field):
    def _normalize(self, value: str) -> str:
        normalized = value.strip()
        if not (normalized.isdigit() and len(normalized) == 10):
            raise ValueError("Phone must contain exactly 10 digits.")
        return normalized


class Address(Field):
    def _normalize(self, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Address is required.")
        return normalized


class Email(Field):
    def _normalize(self, value: str) -> str:
        normalized = value.strip().lower()
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(pattern, normalized):
            raise ValueError("Invalid email format.")

        return normalized


class Birthday(Field):
    def _normalize(self, value: str) -> str:
        normalized = value.strip()

        try:
            parsed_date = datetime.strptime(normalized, "%d.%m.%Y").date()
        except ValueError as error:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from error

        self._date = parsed_date
        return normalized

    @property
    def date(self) -> date:
        return self._date

    def __str__(self) -> str:
        return self._date.strftime("%d.%m.%Y")
