"""Viết tắt khai báo trong tài liệu dạng `<tên> <tham số…>` = `<giá trị>`, kể cả viết tắt có tham số và lồng nhau."""

import re
from dataclasses import dataclass

from reader.text import clean

PAIR = re.compile(r"`(<[^`<>]+>[^`]*)`\s*=\s*`([^`]+)`")
PLACEHOLDER = re.compile(r"<[^<>]+>")
MAX_PASSES = 5


@dataclass
class Abbrev:
    name: str
    pattern: re.Pattern
    template: str
    params: list[str]
    line: int


def _compile(lhs: str) -> tuple[str, re.Pattern, list[str]]:
    name = PLACEHOLDER.match(lhs).group(0)
    rest = lhs[len(name) :]
    params: list[str] = []
    regex = re.escape(name)
    position = 0
    for match in PLACEHOLDER.finditer(rest):
        is_trailing = not rest[match.end() :].strip()
        # Tham số cuối cùng lấy tới hết đoạn code (hoặc hết dòng), không chỉ một ký tự.
        regex += re.escape(rest[position : match.start()]) + ("([^`\n]+)" if is_trailing else "(.+?)")
        params.append(match.group(0))
        position = match.end()
    regex += re.escape(rest[position:])
    return name, re.compile(regex), params


def parse_abbreviations(text: str) -> list[Abbrev]:
    abbrevs: list[Abbrev] = []
    for lineno, line in enumerate(clean(text).split("\n"), start=1):
        for match in PAIR.finditer(line):
            name, pattern, params = _compile(match.group(1))
            abbrevs.append(Abbrev(name, pattern, match.group(2), params, lineno))
    return abbrevs


def definition_lines(text: str) -> set[int]:
    return {a.line for a in parse_abbreviations(text)}


def _apply(text: str, abbrev: Abbrev) -> str:
    def replace(match: re.Match) -> str:
        value = abbrev.template
        for param, captured in zip(abbrev.params, match.groups()):
            value = value.replace(param, captured)
        return value

    return abbrev.pattern.sub(replace, text)


def expand_abbreviations(text: str, abbrevs: list[Abbrev]) -> str:
    ordered = sorted(abbrevs, key=lambda a: len(a.name), reverse=True)
    for _ in range(MAX_PASSES):
        expanded = text
        for abbrev in ordered:
            expanded = _apply(expanded, abbrev)
        if expanded == text:
            break
        text = expanded
    return text
