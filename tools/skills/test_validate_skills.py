from pathlib import Path

from validate_skills import REQUIRED_SECTIONS, main, validate_command, validate_skill

REPO_ROOT = Path(__file__).resolve().parents[2]


def skill_text(name="demo", sections=None, body_extra="", description="Dùng để demo. Use for demo."):
    sections = REQUIRED_SECTIONS if sections is None else sections
    body = "\n\n".join(f"{s}\n\nNội dung." for s in sections)
    return f"---\nname: {name}\ndescription: {description}\nargument-hint: \"\"\n---\n\n# Demo\n\n{body}\n{body_extra}\n"


def make_skill(tmp_path, text, name="demo"):
    d = tmp_path / ".claude" / "skills" / name
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(text, encoding="utf-8", newline="")
    return d


def test_valid_skill_has_no_errors(tmp_path):
    d = make_skill(tmp_path, skill_text())
    assert validate_skill(d, tmp_path) == []


def test_name_must_match_directory(tmp_path):
    d = make_skill(tmp_path, skill_text(name="other"))
    assert any("name" in e for e in validate_skill(d, tmp_path))


def test_missing_section_reported(tmp_path):
    sections = [s for s in REQUIRED_SECTIONS if s != "## Điểm dừng"]
    d = make_skill(tmp_path, skill_text(sections=sections))
    assert any("## Điểm dừng" in e for e in validate_skill(d, tmp_path))


def test_sections_out_of_order_reported(tmp_path):
    sections = list(REQUIRED_SECTIONS)
    sections[0], sections[1] = sections[1], sections[0]
    d = make_skill(tmp_path, skill_text(sections=sections))
    assert any("thứ tự" in e for e in validate_skill(d, tmp_path))


def test_description_too_long(tmp_path):
    d = make_skill(tmp_path, skill_text(description="x" * 1025))
    assert any("description" in e for e in validate_skill(d, tmp_path))


def test_referenced_template_must_exist(tmp_path):
    d = make_skill(tmp_path, skill_text(body_extra="Dùng `templates/x.md` và `tools/y.py`."))
    errors = validate_skill(d, tmp_path)
    assert any("templates/x.md" in e for e in errors)
    assert any("tools/y.py" in e for e in errors)


def test_referenced_files_present_pass(tmp_path):
    d = make_skill(tmp_path, skill_text(body_extra="Dùng `templates/x.md` và `tools/y.py`, ghi `docs/z.md`."))
    (d / "templates").mkdir()
    (d / "templates" / "x.md").write_text("x", encoding="utf-8")
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "y.py").write_text("", encoding="utf-8")
    assert validate_skill(d, tmp_path) == []


def test_validate_skill_accepts_crlf_and_bom(tmp_path):
    d = make_skill(tmp_path, "﻿" + skill_text().replace("\n", "\r\n"))
    assert validate_skill(d, tmp_path) == []


def test_reader_skill_must_mention_reader_view(tmp_path):
    d = make_skill(tmp_path, skill_text(name="detailed-design"), name="detailed-design")
    assert "thiếu bước gọi reader-view" in validate_skill(d, tmp_path)
    fixed = make_skill(tmp_path / "ok", skill_text(name="detailed-design", body_extra="Gọi `reader-view`."), name="detailed-design")
    assert validate_skill(fixed, tmp_path / "ok") == []


def test_other_skill_does_not_need_reader_view(tmp_path):
    d = make_skill(tmp_path, skill_text(name="tdd"), name="tdd")
    assert validate_skill(d, tmp_path) == []


def test_command_requires_description(tmp_path):
    p = tmp_path / "phase-status.md"
    p.write_text("---\nargument-hint: \"\"\n---\n\nNội dung\n", encoding="utf-8")
    assert any("description" in e for e in validate_command(p))


def test_missing_expected_skill_reported(tmp_path, capsys):
    (tmp_path / "tools" / "skills").mkdir(parents=True)
    (tmp_path / "tools" / "skills" / "expected_skills.txt").write_text("ghost\n", encoding="utf-8")
    assert main(tmp_path) == 1
    assert "ghost" in capsys.readouterr().out


def test_repo_skills_are_valid(capsys):
    assert main(REPO_ROOT) == 0
    assert "skill hợp lệ" in capsys.readouterr().out
