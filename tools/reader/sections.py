"""Chia tài liệu thành mục theo heading cấp 2 và 3, mỗi mục có key ổn định và hash nội dung."""

import re
from dataclasses import dataclass

from reader.text import clean, normalize, short_hash

HEADING = re.compile(r"^(#{2,3})\s+(.*?)\s*$")


@dataclass
class Section:
    key: str
    heading: str
    level: int
    body: str
    hash: str


def split_sections(text: str) -> list[Section]:
    lines = clean(text).split("\n")
    raw: list[tuple[str, int, list[str]]] = [("", 0, [])]
    in_fence = False
    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        match = None if in_fence else HEADING.match(line)
        if match:
            raw.append((match.group(2), len(match.group(1)), [line]))
        else:
            raw[-1][2].append(line)

    sections: list[Section] = []
    seen: dict[str, int] = {}
    parent = ""
    for heading, level, body_lines in raw:
        if level == 2:
            parent = heading
        path = f"{parent} › {heading}" if level == 3 else heading
        seen[path] = seen.get(path, 0) + 1
        body = "\n".join(body_lines).strip("\n")
        if level == 0 and not body:
            continue
        sections.append(
            Section(
                key=short_hash(f"{path}#{seen[path]}", 10),
                heading=heading,
                level=level,
                body=body,
                hash=short_hash(normalize(body)),
            )
        )
    return sections
