from __future__ import annotations

from collections import UserDict
from datetime import date, datetime, timedelta

from src.domain.models.record import Record


class AddressBook(UserDict[str, Record]):
    @staticmethod
    def _normalize_key(name: str) -> str:
        return name.strip().lower()

    def add_record(self, record: Record) -> None:
        self.data[self._normalize_key(record.name.value)] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(self._normalize_key(name))

    def delete(self, name: str) -> None:
        key = self._normalize_key(name)

        if key not in self.data:
            raise KeyError("Contact not found.")

        del self.data[key]

    def get_all(self) -> list[Record]:
        return sorted(self.data.values(), key=lambda record: record.name.value.lower())

    def search(self, query: str) -> list[Record]:
        normalized_query = query.strip().lower()

        if not normalized_query:
            return []

        results: list[Record] = []

        for record in self.data.values():
            name_match = normalized_query in record.name.value.lower()
            address_match = (
                record.address is not None
                and normalized_query in record.address.value.lower()
            )
            email_match = (
                record.email is not None
                and normalized_query in record.email.value.lower()
            )
            phone_match = any(
                normalized_query in phone.value for phone in record.phones
            )

            if name_match or address_match or email_match or phone_match:
                results.append(record)

        return sorted(results, key=lambda record: record.name.value.lower())

    def get_upcoming_birthdays(self, days: int = 7) -> list[dict[str, str]]:
        today = date.today()
        end_date = today + timedelta(days=days)
        upcoming: list[dict[str, str]] = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = record.birthday.date
            birthday_this_year = date(today.year, birthday.month, birthday.day)

            if birthday_this_year < today:
                birthday_this_year = date(today.year + 1, birthday.month, birthday.day)

            if today <= birthday_this_year <= end_date:
                congratulation_date = birthday_this_year

                if congratulation_date.weekday() == 5:
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                upcoming.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                    }
                )

        upcoming.sort(
            key=lambda item: datetime.strptime(
                item["congratulation_date"],
                "%d.%m.%Y",
            ).date()
        )

        return upcoming
