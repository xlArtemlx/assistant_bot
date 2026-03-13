from __future__ import annotations

class Note:
    def __init__(self, note: str, tag: str) -> None:
        self.note = note.strip()
        self.tag = tag.strip()

        if not self.note:
            raise ValueError("Note is required.")

    def matches(self, query: str) -> bool:
        normalized_query = query.strip().lower()

        if not normalized_query:
            return False

        return (
            normalized_query in self.note.lower()
            or normalized_query in self.tag.lower()
        )