from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class SQLiteReader:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row

    def rows(self, query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        return [dict(row) for row in self.conn.execute(query, params).fetchall()]

    def one(self, query: str, params: tuple[Any, ...] = ()) -> dict[str, Any] | None:
        row = self.conn.execute(query, params).fetchone()
        return dict(row) if row else None

    def close(self) -> None:
        self.conn.close()
