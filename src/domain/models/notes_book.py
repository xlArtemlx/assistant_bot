from __future__ import annotations

from src.domain.models.note import Note


class NotesBook:
    def __init__(self) -> None:
        self.notes: list[Note] = []

    def add_note(self, note: Note) -> None:
        self.notes.append(note)

    def get_all(self) -> list[Note]:
        return list(self.notes)

    def search(self, query: str) -> list[tuple[int, Note]]:
        results: list[tuple[int, Note]] = []

        for index, note in enumerate(self.notes, start=1):
            if note.matches(query):
                results.append((index, note))

        return results

    def delete_by_index(self, index: int) -> None:
        zero_based_index = index - 1

        if zero_based_index < 0 or zero_based_index >= len(self.notes):
            raise ValueError("Note not found.")

        del self.notes[zero_based_index]

    def get_all_tags(self) -> list[str]:
        tags = set()

        for note in self.notes:
            tags.add(note.tag)

        return sorted(tags)

    def delete_by_tag(self, tag: str) -> int:
        original_count = len(self.notes)
        self.notes = [note for note in self.notes if note.tag != tag]
        deleted_count = original_count - len(self.notes)

        if deleted_count == 0:
            raise ValueError("No notes found with the specified tag.")

        return deleted_count

    def edit_note(self, index: int, new_note: str, new_tag: str) -> None:
        zero_based_index = index - 1

        if zero_based_index < 0 or zero_based_index >= len(self.notes):
            raise ValueError("Note not found.")

        self.notes[zero_based_index] = Note(new_note, new_tag)
