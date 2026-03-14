from __future__ import annotations

import pickle
from abc import ABC, abstractmethod
from pathlib import Path

from src.domain.models.notes_book import NotesBook


class NotesRepository(ABC):
    @abstractmethod
    def load(self) -> NotesBook:
        raise NotImplementedError

    @abstractmethod
    def save(self, notes_book: NotesBook) -> None:
        raise NotImplementedError


class PickleNotesRepository(NotesRepository):
    def __init__(self, filename: str = "notes.pkl") -> None:
        self._path = Path(filename)

    def load(self) -> NotesBook:
        if not self._path.exists():
            return NotesBook()

        with self._path.open("rb") as file:
            return pickle.load(file)

    def save(self, notes_book: NotesBook) -> None:
        with self._path.open("wb") as file:
            pickle.dump(notes_book, file)
