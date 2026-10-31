from pathlib import Path

import pytest

from reader.rewrite import TODO_MARK, Block, format_rewrite, parse_rewrite, sync_rewrite
from reader.sections import split_sections

SRC = "## Một\n\nmột\n\n## Hai\n\nhai\n\n## Ba\n\nba\n"


def rewritten(sections):
    return [Block(s.key, s.hash, f"Đã viết lại {s.heading}.") for s in sections]


def test_sync_keeps_unchanged_block_and_todos_changed():
    old = split_sections(SRC)
    blocks = rewritten(old)
    new_src = SRC.replace("hai\n", "hai đã sửa\n").replace("## Ba\n\nba\n", "") + "## Bốn\n\nbốn\n"
    new = split_sections(new_src)
    synced, todo = sync_rewrite(new, blocks)
    assert [b.key for b in synced] == [s.key for s in new]
    assert synced[0].body == "Đã viết lại Một."
    assert not synced[0].is_todo
    assert synced[1].is_todo and "hai đã sửa" in synced[1].body
    assert synced[2].is_todo and "bốn" in synced[2].body
    assert [s.heading for s in todo] == ["Hai", "Bốn"]


def test_sync_drops_block_with_unknown_key():
    sections = split_sections(SRC)
    blocks = rewritten(sections) + [Block("deadbeef00", "abc", "mục đã xóa")]
    synced, todo = sync_rewrite(sections, blocks)
    assert "deadbeef00" not in [b.key for b in synced]
    assert todo == []


def test_format_parse_roundtrip():
    blocks, _ = sync_rewrite(split_sections(SRC), [])
    text = format_rewrite(blocks)
    assert TODO_MARK in text
    parsed = parse_rewrite(text, Path("x.md"))
    assert [(b.key, b.src_hash, b.body) for b in parsed] == [(b.key, b.src_hash, b.body) for b in blocks]


def test_parse_rewrite_rejects_text_before_first_marker():
    with pytest.raises(ValueError) as exc:
        parse_rewrite("văn bản lạc\n<!-- src-section: abcdef0123 0123456789ab -->\nx\n", Path("auth.md"))
    assert "auth.md" in str(exc.value) and "dòng 1" in str(exc.value)


def test_parse_rewrite_rejects_malformed_marker():
    text = "<!-- src-section: abcdef0123 0123456789ab -->\nx\n\ny\n<!-- src-section: abc -->\nz\n"
    with pytest.raises(ValueError) as exc:
        parse_rewrite(text, Path("auth.md"))
    assert "auth.md" in str(exc.value) and "dòng 5" in str(exc.value)


def test_parse_rewrite_rejects_indented_marker():
    text = "<!-- src-section: abcdef0123 0123456789ab -->\nx\n  <!-- src-section: bcdef01234 0123456789ab -->\ny\n"
    with pytest.raises(ValueError) as exc:
        parse_rewrite(text, Path("auth.md"))
    assert "dòng 3" in str(exc.value)
