"""Kiểm tra bản viết lại không làm mất mã, con số, câu nguyên văn, đoạn code, đường dẫn của bản gốc."""

import re
from pathlib import Path

from reader.abbrev import PAIR
from reader.ids import expand_range, find_refs
from reader.rewrite import Block
from reader.sections import Section
from reader.text import clean, normalize

CODE = re.compile(r"`([^`\n]+)`")
QUOTED = re.compile(r'"([^"\n]+)"|“([^”\n]+)”')
URL = re.compile(r"https?://[^\s`\"')<>]+")
FILE_PATH = re.compile(r"(?<![\w/.-])[\w.-]+(?:/[\w.-]+)*\.(?:md|tsx|ts|py|json|ya?ml|sql|html|css|js)\b")
FENCE = re.compile(r"^```[^\n]*\n(.*?)^```", re.MULTILINE | re.DOTALL)
UNITS = r"phút|giây|giờ|ngày|tuần|tháng|năm|ký tự|lần|byte|ms|KB|MB|GB|px"
NUMBER = re.compile(rf"(?<!\w)(\d+(?:[.,]\d+)*)(?:\s*(%)|\s+({UNITS})(?!\w))?")


def _mask(text: str, pattern: re.Pattern) -> str:
    return pattern.sub(lambda m: " " * len(m.group(0)), text)


def _numbers(line: str) -> set[tuple[str, str]]:
    """Con số kèm đơn vị (nếu có) phải giữ nguyên đơn vị; con số trơn được thỏa bởi cùng số có đơn vị."""
    items = set()
    for m in NUMBER.finditer(line):
        items.add(("con số", m.group(1)))
        unit = m.group(2) or m.group(3)
        if unit:
            items.add(("con số", f"{m.group(1)}{unit}" if unit == "%" else f"{m.group(1)} {unit}"))
    return items


def extract_items(text: str) -> set[tuple[str, str]]:
    """Trả về tập (loại, giá trị đã chuẩn hóa); loại ∈ mã, con số, chuỗi, code, đường dẫn."""
    text = clean(text)
    items: set[tuple[str, str]] = set()
    items |= {("code", normalize(m.group(1))) for m in FENCE.finditer(text)}
    text = _mask(text, FENCE)
    items |= {("code", normalize(m.group(1))) for m in CODE.finditer(text)}
    text = _mask(text, CODE)
    items |= {("chuỗi", normalize(m.group(1) or m.group(2))) for m in QUOTED.finditer(text)}
    text = _mask(text, QUOTED)
    items |= {("đường dẫn", m.group(0).rstrip(".,;:")) for m in URL.finditer(text)}
    text = _mask(text, URL)
    items |= {("đường dẫn", m.group(0)) for m in FILE_PATH.finditer(text)}
    text = _mask(text, FILE_PATH)
    for line in text.split("\n"):
        refs = find_refs(line)
        for ref in refs:
            items |= {("mã", id) for id in expand_range(ref.id)}
        for ref in reversed(refs):
            line = line[: ref.start] + " " * (ref.end - ref.start) + line[ref.end :]
        items |= _numbers(line)
    return items


def _section_label(section: Section) -> str:
    return section.heading or "đầu tài liệu"


def check(src_path: Path, src_text: str, sections: list[Section], blocks: list[Block]) -> list[str]:
    by_key = {b.key: b for b in blocks}
    missing: list[str] = []
    for section in sections:
        body = "\n".join(line for line in section.body.split("\n") if not PAIR.search(line))
        block = by_key.get(section.key)
        have = extract_items(block.body) if block else set()
        lost = extract_items(body) - have
        # Thiếu cả "128" lẫn "128 ký tự" thì chỉ báo "128 ký tự".
        with_unit = {
            value.split(" ")[0].rstrip("%")
            for kind, value in lost
            if kind == "con số" and (" " in value or value.endswith("%"))
        }
        for kind, value in sorted(lost):
            if kind == "con số" and value in with_unit:
                continue
            missing.append(f'- {kind} "{value}" (mục {_section_label(section)})')
    if not missing:
        return []
    return [f"{src_path.as_posix()} – bản đọc thiếu {len(missing)} mục so với bản gốc:", *missing]
