"""Sinh ui-tokens.css từ khối yaml dưới heading `## Tokens` của ui-style.md.

Chạy: py tools/ui/gen_tokens.py docs/design/ui-style.md docs/design/ui-tokens.css
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from simple_yaml import parse  # noqa: E402

HEADER = "/* File sinh tự động từ ui-style.md, không sửa tay. */"


def extract_tokens(md_text: str) -> dict:
    text = md_text.lstrip("﻿").replace("\r\n", "\n")
    heading = re.search(r"^## Tokens\s*$", text, re.MULTILINE)
    if heading:
        block = re.search(r"^```ya?ml\n(.*?)^```", text[heading.end() :], re.MULTILINE | re.DOTALL)
        if block:
            return parse(block.group(1))
    raise ValueError("Không tìm thấy khối ```yaml dưới heading ## Tokens")


def _flatten(tokens: dict, prefix: str = "") -> list[tuple[str, str]]:
    items = []
    for key, value in tokens.items():
        name = f"{prefix}-{key}" if prefix else key
        if isinstance(value, dict):
            items += _flatten(value, name)
        else:
            items.append((name, value))
    return items


def tokens_to_css(tokens: dict) -> str:
    lines = [HEADER, ":root {"]
    lines += [f"  --{name}: {value};" for name, value in _flatten(tokens)]
    lines.append("}")
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Cách dùng: py tools/ui/gen_tokens.py <ui-style.md> <ui-tokens.css>")
        return 2
    source, target = Path(argv[0]), Path(argv[1])
    try:
        css = tokens_to_css(extract_tokens(source.read_text(encoding="utf-8")))
    except ValueError as exc:
        print(f"{source}: {exc}")
        return 1
    target.write_text(css, encoding="utf-8")
    print(f"Đã ghi {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
