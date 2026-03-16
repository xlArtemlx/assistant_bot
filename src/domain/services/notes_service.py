from __future__ import annotations

from src.data.repositories.notes_repository import NotesRepository
from src.domain.models.note import Note
from src.domain.models.notes_book import NotesBook
from src.utils.decorators import input_error


class NotesService:
    def __init__(
        self,
        notes_book: NotesBook,
        repository: NotesRepository,
    ) -> None:
        self._notes_book = notes_book
        self._repository = repository

    @input_error
    def add_note(self, note: str, tag: str) -> str:
        self._notes_book.add_note(Note(note, tag))
        self._repository.save(self._notes_book)
        return "Note added."

    @input_error
    def delete_note(self, index: int) -> str:
        self._notes_book.delete_by_index(index)
        self._repository.save(self._notes_book)
        return "Note deleted."

    @input_error
    def delete_notes_by_tag(self, tag: str) -> str:
        deleted_count = self._notes_book.delete_by_tag(tag)
        self._repository.save(self._notes_book)
        return f"{deleted_count} notes with tag '{tag}' deleted."

    @input_error
    def edit_note(self, index: int, new_note: str, new_tag: str) -> str:
        if not index:
            raise ValueError("Note index is required.")
            
        self._notes_book.edit_note(int(index), new_note, new_tag)
        self._repository.save(self._notes_book)
        return "Note updated."

    def get_all_notes(self) -> list[tuple[int, Note]]:
        return list(enumerate(self._notes_book.get_all(), start=1))

    def search_notes(self, query: str) -> list[tuple[int, Note]]:
        return self._notes_book.search(query)

    def get_all_tags(self) -> list[str]:
        return self._notes_book.get_all_tags()
