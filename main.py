from __future__ import annotations

from src.app.application import Application
from src.app.context import AppContext
from src.data.repositories.address_book_repository import PickleAddressBookRepository
from src.data.repositories.notes_repository import PickleNotesRepository
from src.domain.services.birthday_service import BirthdayService
from src.domain.services.contact_service import ContactService
from src.domain.services.notes_service import NotesService


def main() -> None:
    address_book_repository = PickleAddressBookRepository()
    notes_repository = PickleNotesRepository()

    book = address_book_repository.load()
    notes_book = notes_repository.load()

    context = AppContext(
        book=book,
        notes_book=notes_book,
        address_book_repository=address_book_repository,
        notes_repository=notes_repository,
        contact_service=ContactService(book, address_book_repository),
        birthday_service=BirthdayService(book, address_book_repository),
        notes_service=NotesService(notes_book, notes_repository),
    )

    app = Application(context)
    app.run()

if __name__ == "__main__":
    main()