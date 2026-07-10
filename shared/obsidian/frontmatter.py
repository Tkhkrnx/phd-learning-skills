from __future__ import annotations

from datetime import datetime


def build_frontmatter(title: str, paper_id: str, note_id: str, cache_dir: str | None) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    title = (title or "").replace('"', "'")
    cache_dir = (cache_dir or "").replace('"', "'")
    return (
        "---\n"
        f'paper_id: "{paper_id}"\n'
        f'paperquay_note_id: "{note_id}"\n'
        f'title: "{title}"\n'
        'source_type: "paperquay"\n'
        f'cache_dir: "{cache_dir}"\n'
        f'created: "{today}"\n'
        f'updated: "{today}"\n'
        "---\n"
    )
