from __future__ import annotations

from unittest.mock import Mock

import pytest

from src.domain.models.record import Record
from src.domain.services.contact_service import ContactService


@pytest.fixture
def repository() -> Mock:
    return Mock()


@pytest.fixture
def book() -> Mock:
    return Mock()


@pytest.fixture
def service(book: Mock, repository: Mock) -> ContactService:
    return ContactService(book=book, repository=repository)


def test_add_contact_creates_new_record_and_saves(
    service: ContactService,
    book: Mock,
    repository: Mock,
) -> None:
    book.find.return_value = None

    result = service.add_contact(
        name="John",
        address="Main street",
        phone="1234567890",
        email="john@example.com",
    )

    assert result == "Contact added."
    book.add_record.assert_called_once()
    repository.save.assert_called_once_with(book)

    created_record = book.add_record.call_args[0][0]
    assert isinstance(created_record, Record)
    assert created_record.name.value == "John"


def test_add_contact_updates_existing_contact_and_saves(
    service: ContactService,
    book: Mock,
    repository: Mock,
) -> None:
    record = Mock()
    book.find.return_value = record

    result = service.add_contact(
        name="John",
        address="New address",
        phone="1234567890",
        email="john@example.com",
    )

    assert result == "Contact updated."
    record.set_address.assert_called_once_with("New address")
    record.add_phone.assert_called_once_with("1234567890")
    record.set_email.assert_called_once_with("john@example.com")
    repository.save.assert_called_once_with(book)


def test_add_contact_skips_empty_optional_fields(
    service: ContactService,
    book: Mock,
    repository: Mock,
) -> None:
    record = Mock()
    book.find.return_value = record

    result = service.add_contact(
        name="John",
        address="   ",
        phone="",
        email="   ",
    )

    assert result == "Contact updated."
    record.set_address.assert_not_called()
    record.add_phone.assert_not_called()
    record.set_email.assert_not_called()
    repository.save.assert_called_once_with(book)


def test_edit_contact_name_renames_contact_and_saves(
    service: ContactService,
    book: Mock,
    repository: Mock,
) -> None:
    record = Mock()
    book.find.side_effect = [record, None]

    result = service.edit_contact_name("John", "Johnny")

    assert result == "Contact name updated."
    book.delete.assert_called_once_with("John")
    record.rename.assert_called_once_with("Johnny")
    book.add_record.assert_called_once_with(record)
    repository.save.assert_called_once_with(book)


def test_edit_contact_name_returns_nothing_changed_for_same_name(
    service: ContactService,
    book: Mock,
    repository: Mock,
) -> None:
    record = Mock()
    book.find.return_value = record

    result = service.edit_contact_name("John", "  john  ")

    assert result == "Nothing changed."
    book.delete.assert_not_called()
    repository.save.assert_not_called()


def test_edit_contact_name_returns_error_when_new_name_already_exists(
    service: ContactService,
    book: Mock,
    repository: Mock,
) -> None:
    current_record = Mock()
    existing_record = Mock()
    book.find.side_effect = [current_record, existing_record]

    result = service.edit_contact_name("John", "Jane")

    assert result == "A contact with this name already exists."
    book.delete.assert_not_called()
    repository.save.assert_not_called()


def test_add_phone_saves_and_returns_message(
    service: ContactService,
    book: Mock,
    repository: Mock,
) -> None:
    record = Mock()
    book.find.return_value = record

    result = service.add_phone("John", "1234567890")

    assert result == "Phone added."
    record.add_phone.assert_called_once_with("1234567890")
    repository.save.assert_called_once_with(book)


def test_delete_contact_saves_and_returns_message(
    service: ContactService,
    book: Mock,
    repository: Mock,
) -> None:
    result = service.delete_contact("John")

    assert result == "Contact deleted."
    book.delete.assert_called_once_with("John")
    repository.save.assert_called_once_with(book)


def test_get_contact_details_returns_record(
    service: ContactService,
    book: Mock,
) -> None:
    record = Mock()
    book.find.return_value = record

    result = service.get_contact_details("John")

    assert result is record


def test_search_contacts_returns_book_search_result(
    service: ContactService,
    book: Mock,
) -> None:
    expected = [Mock(), Mock()]
    book.search.return_value = expected

    result = service.search_contacts("jo")

    assert result == expected
    book.search.assert_called_once_with("jo")
