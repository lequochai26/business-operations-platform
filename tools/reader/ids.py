"""Nhận diện mã (quy tắc, test case, vấn đề, task, review, câu hỏi mở, ADR) và lập bảng mã → ý nghĩa ngắn."""

import re
from dataclasses import dataclass, field
from pathlib import Path

from reader.sections import split_sections
from reader.text import read_text

RULE = r"R-[A-Z]{3}-\d{2}"
CASE = r"P\d-[A-Z]{3}-\d{3}"
TASK = r"(?<![\w-])T\d{2}(?![\w-])"
REVIEW = r"RV-\d{2}"
ADR = r"ADR \d{4}"
OPEN_QUESTION = r"(?i:câu hỏi mở) \d+"

RANGE_RE = re.compile(r"(R-[A-Z]{3})-(\d{2})\s*(?:…|\.\.\.)\s*\1-(\d{2})")
REF_RE = re.compile("|".join(f"(?:{p})" for p in (RULE, CASE, REVIEW, ADR, OPEN_QUESTION, TASK)))
CODE_RE = re.compile(r"`[^`\n]*`")

RULE_DEF = re.compile(rf"^\s*- ({RULE}): (.*)$")
HEADING_DEF = re.compile(rf"^#{{2,3}} ({CASE}|{REVIEW}|T\d{{2}})(?:\s*[:–-])?\s+(.*)$")
OPEN_QUESTION_DEF = re.compile(r"^\s*- \[[ xX]\] (\d+)\. (.*)$")
ADR_TITLE = re.compile(r"^# (\d{4})\s*[–-]\s*(.*)$")

GLOSS_MAX = 60
GLOSS_STOP = re.compile(r"[→:;.,]")


@dataclass
class Ref:
    id: str
    start: int
    end: int


@dataclass
class Definition:
    id: str
    gloss: str
    source: Path
    section_key: str


def _canonical(raw: str) -> str:
    return raw.lower() if raw.lower().startswith("câu hỏi mở") else raw


def find_refs(line: str) -> list[Ref]:
    masked = CODE_RE.sub(lambda m: " " * len(m.group(0)), line)
    refs: list[Ref] = []
    taken: list[tuple[int, int]] = []
    for m in RANGE_RE.finditer(masked):
        refs.append(Ref(f"{m.group(1)}-{m.group(2)}..{m.group(1)}-{m.group(3)}", m.start(), m.end()))
        taken.append((m.start(), m.end()))
    for m in REF_RE.finditer(masked):
        if any(s <= m.start() < e for s, e in taken):
            continue
        refs.append(Ref(_canonical(m.group(0)), m.start(), m.end()))
    return sorted(refs, key=lambda r: r.start)


def expand_range(id: str) -> list[str]:
    if ".." not in id:
        return [id]
    first, last = id.split("..")
    prefix = first[:-2]
    return [f"{prefix}{n:02d}" for n in range(int(first[-2:]), int(last[-2:]) + 1)]


def short_gloss(text: str) -> str:
    previous = None
    while previous != text:
        previous, text = text, re.sub(r"\([^()]*\)", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    stop = GLOSS_STOP.search(text)
    if stop:
        text = text[: stop.start()].strip()
    if len(text) > GLOSS_MAX:
        text = text[: GLOSS_MAX - 1].rstrip() + "…"
    return text


def _title(text: str) -> str:
    text = text.strip()
    return text if len(text) <= GLOSS_MAX else text[: GLOSS_MAX - 1].rstrip() + "…"


def _phase_dir(path: Path) -> Path | None:
    for parent in [path, *path.parents]:
        if parent.parent.name == "phases" and parent.name.startswith("phase-"):
            return parent
    return None


def _scoped_candidates(from_source: Path) -> list[Path]:
    candidates = [from_source]
    phase = _phase_dir(from_source)
    if phase is not None:
        slug = from_source.stem.removesuffix("-review")
        candidates += [phase / "design" / f"{slug}.md", phase / "design" / "reviews" / f"{slug}-review.md"]
    return candidates


@dataclass
class Index:
    global_defs: dict[str, Definition] = field(default_factory=dict)
    phase_defs: dict[tuple[Path, str], Definition] = field(default_factory=dict)
    file_defs: dict[tuple[Path, str], Definition] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def _add(self, table: dict, key, definition: Definition) -> None:
        if key in table:
            first = table[key]
            self.warnings.append(f"{definition.id} được định nghĩa nhiều lần: {first.source} và {definition.source}")
            return
        table[key] = definition

    @classmethod
    def build(cls, docs_root: Path, sources: list[Path]) -> "Index":
        index = cls()
        for source in sources:
            text = read_text(source)
            if source.parent.name == "decisions":
                first = next((line for line in text.split("\n") if line.startswith("# ")), "")
                if match := ADR_TITLE.match(first):
                    definition = Definition(f"ADR {match.group(1)}", _title(match.group(2)), source, "")
                    index._add(index.global_defs, definition.id, definition)
            for section in split_sections(text):
                in_open_questions = section.heading.strip().lower() == "câu hỏi mở"
                for line in section.body.split("\n"):
                    if match := RULE_DEF.match(line):
                        definition = Definition(match.group(1), short_gloss(match.group(2)), source, section.key)
                        index._add(index.global_defs, definition.id, definition)
                    elif match := HEADING_DEF.match(line):
                        id = match.group(1)
                        definition = Definition(id, _title(match.group(2)), source, section.key)
                        if id.startswith("T"):
                            index._add(index.phase_defs, (_phase_dir(source), id), definition)
                        elif id.startswith("RV-"):
                            index._add(index.file_defs, (source, id), definition)
                        else:
                            index._add(index.global_defs, id, definition)
                    elif in_open_questions and (match := OPEN_QUESTION_DEF.match(line)):
                        id = f"câu hỏi mở {match.group(1)}"
                        definition = Definition(id, short_gloss(match.group(2)), source, section.key)
                        index._add(index.file_defs, (source, id), definition)
        return index

    def resolve(self, id: str, from_source: Path) -> Definition | None:
        if id.startswith("T"):
            return self.phase_defs.get((_phase_dir(from_source), id))
        if id.startswith("RV-") or id.startswith("câu hỏi mở"):
            for candidate in _scoped_candidates(from_source):
                if definition := self.file_defs.get((candidate, id)):
                    return definition
            return None
        return self.global_defs.get(id)
