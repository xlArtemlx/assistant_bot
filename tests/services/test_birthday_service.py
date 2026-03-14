from __future__ import annotations

from unittest.mock import Mock

import pytest

from src.domain.services.birthday_service import BirthdayService


@pytest.fixture
def repository() -> Mock:
    return Mock()


@pytest.fixture
def book() -> Mock:
    return Mock()


@pytest.fixture
def service(book: Mock, repository: Mock) -> BirthdayService:
    return BirthdayService(book=book, repository=repository)


def test_add_or_update_birthday_saves_and_returns_message(
    service: BirthdayService,
    book: Mock,
    repository: Mock,
) -> None:
    record = Mock()
    book.find.return_value = record

    result = service.add_or_update_birthday("John", "10.10.1990")

    assert result == "Birthday saved."
    book.find.assert_called_once_with("John")
    record.add_birthday.assert_called_once_with("10.10.1990")
    repository.save.assert_called_once_with(book)


def test_add_or_update_birthday_returns_not_found_error_when_contact_missing(
    service: BirthdayService,
    book: Mock,
    repository: Mock,
) -> None:
    book.find.return_value = None

    result = service.add_or_update_birthday("John", "10.10.1990")

    assert result == "Contact not found."
    repository.save.assert_not_called()


def test_get_birthday_returns_birthday_string(
    service: BirthdayService,
    book: Mock,
) -> None:
    record = Mock()
    record.birthday = "10.10.1990"
    book.find.return_value = record

    result = service.get_birthday("John")

    assert result == "10.10.1990"


def test_get_birthday_returns_not_set_when_missing(
    service: BirthdayService,
    book: Mock,
) -> None:
    record = Mock()
    record.birthday = None
    book.find.return_value = record

    result = service.get_birthday("John")

    assert result == "Birthday not set."


def test_get_upcoming_birthdays_grouped_returns_sorted_grouped_result(
    service: BirthdayService,
    book: Mock,
) -> None:
    book.get_upcoming_birthdays.return_value = [
        {"name": "Anna", "congratulation_date": "15.03.2026"},
        {"name": "John", "congratulation_date": "14.03.2026"},
        {"name": "Bob", "congratulation_date": "15.03.2026"},
    ]

    result = service.get_upcoming_birthdays_grouped(7)

    assert result == [
        ("14.03.2026", "John"),
        ("15.03.2026", "Anna, Bob"),
    ]
    book.get_upcoming_birthdays.assert_called_once_with(days=7)


def test_get_upcoming_birthdays_grouped_returns_empty_list_when_no_birthdays(
    service: BirthdayService,
    book: Mock,
) -> None:
    book.get_upcoming_birthdays.return_value = []

    result = service.get_upcoming_birthdays_grouped(7)

    assert result == []


@pytest.mark.parametrize(
    ("days", "expected"),
    [
        ("7", 7),
        ("0", 0),
        (5, 5),
    ],
)
def test_get_upcoming_birthdays_grouped_parses_valid_days(
    service: BirthdayService,
    book: Mock,
    days: str | int,
    expected: int,
) -> None:
    book.get_upcoming_birthdays.return_value = []

    service.get_upcoming_birthdays_grouped(days)

    book.get_upcoming_birthdays.assert_called_once_with(days=expected)


@pytest.mark.parametrize(
    "days",
    ["", "abc", "-1", -1],
)
def test_get_upcoming_birthdays_grouped_returns_validation_error_for_invalid_days(
    service: BirthdayService,
    days: str | int,
) -> None:
    result = service.get_upcoming_birthdays_grouped(days)

    if days == "":
        assert result == "Number of days is required."
    elif days in {"abc", "-1"}:
        assert result == "Number of days must be a positive integer."
    else:
        assert result == "Number of days cannot be negative."