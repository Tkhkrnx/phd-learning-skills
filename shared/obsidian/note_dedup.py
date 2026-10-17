"""Read-only comparison aid; identity, absorption and retention require review."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


IMAGE = re.compile(r'!\[([^\]\n]*)\]\((<[^>\n]+>|[^)\n]+)\)')


def note_profile(path: Path) -> dict:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    frontmatter = {}
    match = re.match(r'\A---\n(.*?)\n---(?:\n|$)', text, re.S)
    if match:
        try:
            frontmatter = yaml.safe_load(match[1]) or {}
        except yaml.YAMLError:
            frontmatter = {"unparsed": match[1]}
        text = text[match.end():]
    images = []

    def image_identity(match: re.Match) -> str:
        value = match[2].strip()
        href = value[1:value.index('>')] if value.startswith('<') else value.split(' "', 1)[0]
        title = value[value.index('>') + 1:] if value.startswith('<') else value[len(href):]
        entry = {"alt": match[1], "reference": href, "sha256": None}
        if not re.match(r'^(https?|data):', href, re.I):
            if href.lower().startswith('file:'):
                href = urlsplit(href).path
                if re.match(r'^/[A-Za-z]:/', href):
                    href = href[1:]
            local = Path(unquote(href))
            if not local.is_absolute():
                local = path.parent / local
            if local.is_file():
                entry["sha256"] = hashlib.sha256(local.read_bytes()).hexdigest()
        images.append(entry)
        # Keep alt/title text; only replace the image's storage target.
        return f'![{match[1]}](<IMAGE_TARGET>{title})'

    # Storage normalization never rewrites fenced or inline code examples.
    pieces = re.split(r'(```.*?```|~~~.*?~~~|`[^`\n]+`)', text, flags=re.S)
    normalized = ''.join(piece if index % 2 else IMAGE.sub(image_identity, piece)
                         for index, piece in enumerate(pieces))
    normalized = '\n'.join(line.rstrip() for line in normalized.splitlines()).strip()
    normalized = re.sub(r'\n{3,}', '\n\n', normalized)
    return {"path": str(path.resolve()), "sha256": hashlib.sha256(raw).hexdigest(),
            "modified_ns": path.stat().st_mtime_ns, "frontmatter": frontmatter,
            "body": normalized, "images": images}


def compare_notes(candidate: Path, existing: Path) -> dict:
    left, right = note_profile(candidate), note_profile(existing)
    body_equal = left["body"] == right["body"]
    verified = all(img["sha256"] is not None for profile in (left, right) for img in profile["images"])
    image_hashes_equal = verified and [img["sha256"] for img in left["images"]] == [
        img["sha256"] for img in right["images"]]
    return {"candidate": {k:v for k,v in left.items() if k != "body"},
            "existing": {k:v for k,v in right.items() if k != "body"},
            "raw_bytes_equal": left["sha256"] == right["sha256"],
            "body_equal_after_storage_normalization": body_equal,
            "all_image_bytes_verified": verified,
            "image_bytes_equal": image_hashes_equal,
            "equivalent_body_and_images": body_equal and image_hashes_equal,
            "frontmatter_equal": left["frontmatter"] == right["frontmatter"],
            "evidence_limit": "Does not infer paper identity, semantic absorption, finality, "
                              "or permission to import/overwrite/delete. mtime is not authority."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--existing", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(compare_notes(args.candidate, args.existing), ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
