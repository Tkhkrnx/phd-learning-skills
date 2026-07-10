from __future__ import annotations

from pathlib import Path

from .sqlite_reader import SQLiteReader


class NoteMatcher:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.reader = SQLiteReader(self.root / "paperquay-notes.sqlite")

    def by_note_id(self, note_id: str) -> dict | None:
        return self.reader.one("select * from notes where id = ?", (note_id,))

    def by_paper_id(self, paper_id: str) -> list[dict]:
        return self.reader.rows(
            "select * from notes where paper_id = ? order by updated_at desc",
            (paper_id,),
        )

    def search(self, text: str) -> list[dict]:
        pattern = f"%{text}%"
        return self.reader.rows(
            "select * from notes where title like ? or content_text like ? order by updated_at desc",
            (pattern, pattern),
        )

    def close(self) -> None:
        self.reader.close()
