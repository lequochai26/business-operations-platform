"""Định dạng bản viết lại (docs/reader/_rewrite/): mỗi mục gốc là một khối mở đầu bằng marker."""

import re
from dataclasses import dataclass
from pathlib import Path

from reader.sections import Section
from reader.text import clean

TODO_MARK = "<!-- TODO: viết lại mục này -->"
MARKER_PREFIX = "<!-- src-section:"
MARKER = re.compile(r"^<!-- src-section: (\S+) (\S+) -->$")


@dataclass
class Block:
    key: str
    src_hash: str
    body: str
    line: int = 0  # dòng của marker trong file bản viết lại (0 nếu khối được tạo trong bộ nhớ)

    @property
    def is_todo(self) -> bool:
        return TODO_MARK in self.body


def parse_rewrite(text: str, path: Path) -> list[Block]:
    blocks: list[Block] = []
    body: list[str] = []
    for lineno, line in enumerate(clean(text).split("\n"), start=1):
        if line.lstrip().startswith(MARKER_PREFIX) and not line.startswith(MARKER_PREFIX):
            raise ValueError(f"{path}, dòng {lineno}: marker bị thụt lề, marker phải nằm ở đầu dòng")
        if line.startswith(MARKER_PREFIX):
            match = MARKER.match(line)
            if not match:
                raise ValueError(f"{path}, dòng {lineno}: marker sai cú pháp: {line}")
            if blocks:
                blocks[-1].body = "\n".join(body).strip("\n")
            blocks.append(Block(match.group(1), match.group(2), "", lineno))
            body = []
        elif not blocks:
            if line.strip():
                raise ValueError(f"{path}, dòng {lineno}: có nội dung trước marker đầu tiên")
        else:
            body.append(line)
    if blocks:
        blocks[-1].body = "\n".join(body).strip("\n")
    return blocks


def format_rewrite(blocks: list[Block]) -> str:
    return "\n".join(f"<!-- src-section: {b.key} {b.src_hash} -->\n{b.body.strip(chr(10))}\n" for b in blocks)


def _todo_block(section: Section) -> Block:
    return Block(section.key, section.hash, f"{TODO_MARK}\n{section.body}")


def sync_rewrite(sections: list[Section], blocks: list[Block]) -> tuple[list[Block], list[Section]]:
    """Giữ khối của mục chưa đổi; mục mới hoặc đã đổi thành khối TODO; bỏ khối của mục đã xóa."""
    existing = {b.key: b for b in blocks}
    synced: list[Block] = []
    todo: list[Section] = []
    for section in sections:
        block = existing.get(section.key)
        if block is None or block.src_hash != section.hash:
            block = _todo_block(section)
        synced.append(block)
        if block.is_todo:
            todo.append(section)
    return synced, todo
