from reader.sections import split_sections

DOC = "# Tiêu đề\n\nMở đầu.\n\n## A\n\nNội dung A.\n\n### A1\n\nNội dung A1.\n\n## B\n\nNội dung B.\n"


def test_split_sections_levels():
    sections = split_sections(DOC)
    assert [s.heading for s in sections] == ["", "A", "A1", "B"]
    assert [s.level for s in sections] == [0, 2, 3, 2]
    assert "# Tiêu đề" in sections[0].body


def test_split_sections_duplicate_headings_get_distinct_keys():
    doc = "## A\n\n### Quy tắc\n\nx\n\n## B\n\n### Quy tắc\n\ny\n"
    first = split_sections(doc)
    rules = [s for s in first if s.heading == "Quy tắc"]
    assert len(rules) == 2
    assert rules[0].key != rules[1].key
    assert [s.key for s in split_sections(doc)] == [s.key for s in first]


def test_section_hash_ignores_crlf_and_bom():
    plain = split_sections(DOC)
    windows = split_sections("﻿" + DOC.replace("\n", "\r\n"))
    assert [s.hash for s in windows] == [s.hash for s in plain]
    assert [s.key for s in windows] == [s.key for s in plain]


def test_section_hash_changes_when_body_changes():
    before = split_sections(DOC)
    after = split_sections(DOC.replace("Nội dung A1.", "Nội dung A1 đã sửa."))
    assert before[2].hash != after[2].hash
    assert before[1].hash == after[1].hash
