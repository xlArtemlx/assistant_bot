from __future__ import annotations

import pickle
from abc import ABC, abstractmethod
from pathlib import Path

from src.domain.models.address_book import AddressBook


class AddressBookRepository(ABC):
    @abstractmethod
    def load(self) -> AddressBook:
        raise NotImplementedError

    @abstractmethod
    def save(self, book: AddressBook) -> None:
        raise NotImplementedError


class PickleAddressBookRepository(AddressBookRepository):
    def __init__(self, filename: str = "addressbook.pkl") -> None:
        self._path = Path(filename)

    def load(self) -> AddressBook:
        if not self._path.exists():
            return AddressBook()

        with self._path.open("rb") as file:
            return pickle.load(file)

    def save(self, book: AddressBook) -> None:
        with self._path.open("wb") as file:
            pickle.dump(book, file)
