from __future__ import annotations

import argparse
import json

from shared.obsidian.note_search import search_vault_notes
from shared.obsidian.vault_paths import DEFAULT_VAULT


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", default=str(DEFAULT_VAULT))
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    hits = search_vault_notes(query=args.query, vault=DEFAULT_VAULT.__class__(args.vault), limit=args.limit)
    print(json.dumps({"query": args.query, "hits": hits[: args.limit]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
