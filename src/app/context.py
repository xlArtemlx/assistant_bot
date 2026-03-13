from __future__ import annotations

from dataclasses import dataclass

from src.data.repositories.address_book_repository import AddressBookRepository
from src.data.repositories.notes_repository import NotesRepository
from src.domain.models.address_book import AddressBook
from src.domain.models.notes_book import NotesBook
from src.domain.services.birthday_service import BirthdayService
from src.domain.services.contact_service import ContactService
from src.domain.services.notes_service import NotesService


@dataclass
class AppContext:
    book: AddressBook
    notes_book: NotesBook
    address_book_repository: AddressBookRepository
    notes_repository: NotesRepository
    contact_service: ContactService
    birthday_service: BirthdayService
    notes_service: NotesService