"""Kiểm tra cấu trúc các skill trong .claude/skills theo spec docs/process/2026-10-29-dev-process-skills-design.md.

Chạy: py tools/skills/validate_skills.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from simple_yaml import parse  # noqa: E402

REQUIRED_SECTIONS = [
    "## Mục đích",
    "## Điều kiện tiên quyết",
    "## Input",
    "## Các bước",
    "## Điểm dừng",
    "## Output",
    "## Tự kiểm tra",
    "## Cập nhật status.md",
    "## Báo cáo kết thúc",
]
MAX_DESCRIPTION = 1024
SKILL_RELATIVE = re.compile(r"^(templates|checklists|scripts)/\S+$")
REPO_RELATIVE = re.compile(r"^(\.claude|tools)/\S+$")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").lstrip("﻿").replace("\r\n", "\n")


def _frontmatter(text: str) -> tuple[dict | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    return parse(text[4:end]), text[end + 5 :]


def _check_description(meta: dict) -> list[str]:
    desc = meta.get("description", "")
    if not desc:
        return ["thiếu description trong frontmatter"]
    if len(desc) > MAX_DESCRIPTION:
        return [f"description dài {len(desc)} ký tự, tối đa {MAX_DESCRIPTION}"]
    return []


def _check_sections(body: str) -> list[str]:
    headings = [line.strip() for line in body.split("\n") if line.startswith("## ")]
    errors = [f"thiếu heading {s}" for s in REQUIRED_SECTIONS if s not in headings]
    present = [h for h in headings if h in REQUIRED_SECTIONS]
    if not errors and present != REQUIRED_SECTIONS:
        errors.append("các heading bắt buộc sai thứ tự: " + ", ".join(present))
    return errors


def _check_references(body: str, skill_dir: Path, repo_root: Path) -> list[str]:
    errors = []
    for ref in sorted(set(re.findall(r"`([^`\s]+)`", body))):
        if SKILL_RELATIVE.match(ref):
            target = skill_dir / ref
        elif REPO_RELATIVE.match(ref):
            target = repo_root / ref
        else:
            continue
        if not target.exists():
            errors.append(f"file được nhắc tới không tồn tại: {ref}")
    return errors


def validate_skill(skill_dir: Path, repo_root: Path) -> list[str]:
    path = skill_dir / "SKILL.md"
    if not path.exists():
        return ["thiếu SKILL.md"]
    meta, body = _frontmatter(read_text(path))
    if meta is None:
        return ["thiếu frontmatter"]
    errors = []
    if meta.get("name") != skill_dir.name:
        errors.append(f"name '{meta.get('name')}' không trùng tên thư mục '{skill_dir.name}'")
    errors += _check_description(meta)
    if "argument-hint" not in meta:
        errors.append("thiếu argument-hint trong frontmatter")
    errors += _check_sections(body)
    errors += _check_references(body, skill_dir, repo_root)
    return errors


def validate_command(path: Path) -> list[str]:
    meta, _ = _frontmatter(read_text(path))
    if meta is None:
        return ["thiếu frontmatter"]
    return _check_description(meta)


def main(repo_root: Path) -> int:
    expected_file = repo_root / "tools" / "skills" / "expected_skills.txt"
    names = [n.strip() for n in read_text(expected_file).split("\n") if n.strip()] if expected_file.exists() else []
    failures = 0
    for name in names:
        for error in validate_skill(repo_root / ".claude" / "skills" / name, repo_root):
            print(f"{name}: {error}")
            failures += 1
    commands = 0
    command = repo_root / ".claude" / "commands" / "phase-status.md"
    if command.exists():
        commands = 1
        for error in validate_command(command):
            print(f"phase-status: {error}")
            failures += 1
    if failures:
        return 1
    print(f"{len(names)} skill hợp lệ, {commands} command hợp lệ")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(__file__).resolve().parents[2]))
