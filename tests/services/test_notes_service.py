from __future__ import annotations

from unittest.mock import Mock

from src.domain.models.note import Note
from src.domain.services.notes_service import NotesService


import pytest


@pytest.fixture
def repository() -> Mock:
    return Mock()


@pytest.fixture
def notes_book() -> Mock:
    return Mock()


@pytest.fixture
def service(notes_book: Mock, repository: Mock) -> NotesService:
    return NotesService(notes_book=notes_book, repository=repository)


def test_add_note_saves_note_and_returns_message(
    service: NotesService,
    notes_book: Mock,
    repository: Mock,
) -> None:
    result = service.add_note("Buy milk", "personal")

    assert result == "Note added."
    notes_book.add_note.assert_called_once()

    added_note = notes_book.add_note.call_args[0][0]
    assert isinstance(added_note, Note)
    assert added_note.note == "Buy milk"
    assert added_note.tag == "personal"

    repository.save.assert_called_once_with(notes_book)


def test_delete_note_saves_and_returns_message(
    service: NotesService,
    notes_book: Mock,
    repository: Mock,
) -> None:
    result = service.delete_note(1)

    assert result == "Note deleted."
    notes_book.delete_by_index.assert_called_once_with(1)
    repository.save.assert_called_once_with(notes_book)


def test_delete_notes_by_tag_saves_and_returns_deleted_count(
    service: NotesService,
    notes_book: Mock,
    repository: Mock,
) -> None:
    notes_book.delete_by_tag.return_value = 3

    result = service.delete_notes_by_tag("work")

    assert result == "3 notes with tag 'work' deleted."
    notes_book.delete_by_tag.assert_called_once_with("work")
    repository.save.assert_called_once_with(notes_book)


def test_edit_note_saves_and_returns_message(
    service: NotesService,
    notes_book: Mock,
    repository: Mock,
) -> None:
    result = service.edit_note(2, "New text", "new-tag")

    assert result == "Note updated."
    notes_book.edit_note.assert_called_once_with(2, "New text", "new-tag")
    repository.save.assert_called_once_with(notes_book)


def test_get_all_notes_returns_enumerated_notes(
    service: NotesService,
    notes_book: Mock,
) -> None:
    first = Mock()
    second = Mock()
    notes_book.get_all.return_value = [first, second]

    result = service.get_all_notes()

    assert result == [(1, first), (2, second)]


def test_search_notes_returns_notes_book_search_result(
    service: NotesService,
    notes_book: Mock,
) -> None:
    expected = [(1, Mock())]
    notes_book.search.return_value = expected

    result = service.search_notes("milk")

    assert result == expected
    notes_book.search.assert_called_once_with("milk")


def test_get_all_tags_returns_tags(
    service: NotesService,
    notes_book: Mock,
) -> None:
    notes_book.get_all_tags.return_value = ["work", "personal"]

    result = service.get_all_tags()

    assert result == ["work", "personal"]
    notes_book.get_all_tags.assert_called_once()