from __future__ import annotations

from pathlib import Path

from .sqlite_reader import SQLiteReader


class LibraryReader:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.sqlite_path = self.root / "paperquay-library.sqlite"
        self.reader = SQLiteReader(self.sqlite_path)

    def get_paper(self, paper_id: str) -> dict | None:
        paper = self.reader.one("select * from papers where id = ?", (paper_id,))
        if not paper:
            return None
        paper["authors"] = self.reader.rows(
            "select * from authors where paper_id = ? order by sort_order",
            (paper_id,),
        )
        paper["attachments"] = self.reader.rows(
            "select * from attachments where paper_id = ? order by created_at",
            (paper_id,),
        )
        paper["keywords"] = [
            row["keyword"]
            for row in self.reader.rows(
                "select keyword from paper_keywords where paper_id = ? order by sort_order",
                (paper_id,),
            )
        ]
        return paper

    def close(self) -> None:
        self.reader.close()
