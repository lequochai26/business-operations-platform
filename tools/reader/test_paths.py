from reader.paths import html_path, reader_path, rewrite_path, select_sources, source_files


def make_docs(tmp_path):
    docs = tmp_path / "docs"
    for rel in [
        "phases/phase-0/design/auth.md",
        "phases/phase-0/status.md",
        "phases/phase-1/status.md",
        "design/db-schema.md",
        "decisions/0001-x.md",
        "testing/viewpoints.md",
        "project/01-overview.md",
        "reader/phases/phase-0/status.md",
    ]:
        p = docs / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("x", encoding="utf-8")
    return docs


def test_source_files_scope(tmp_path):
    docs = make_docs(tmp_path)
    rels = [p.relative_to(docs).as_posix() for p in source_files(docs)]
    assert "project/01-overview.md" not in rels
    assert not any(r.startswith("reader/") for r in rels)
    assert "phases/phase-0/design/auth.md" in rels and "decisions/0001-x.md" in rels
    assert len(rels) == 6


def test_select_sources_phase_and_all(tmp_path):
    docs = make_docs(tmp_path)
    assert len(select_sources(docs, ["all"])) == 6
    phase0 = [p.relative_to(docs).as_posix() for p in select_sources(docs, ["phase-0"])]
    assert phase0 == ["phases/phase-0/design/auth.md", "phases/phase-0/status.md"]
    one = select_sources(docs, [str(docs / "design/db-schema.md")])
    assert one == [docs / "design/db-schema.md"]


def test_select_sources_accepts_relative_file_path(tmp_path, monkeypatch):
    docs = make_docs(tmp_path)
    monkeypatch.chdir(tmp_path)
    assert select_sources(docs, ["docs/design/db-schema.md"]) == [docs / "design/db-schema.md"]


def test_reader_and_rewrite_paths(tmp_path):
    docs = tmp_path / "docs"
    src = docs / "phases/phase-0/design/auth.md"
    assert reader_path(docs, src) == docs / "reader/phases/phase-0/design/auth.md"
    assert rewrite_path(docs, src) == docs / "reader/_rewrite/phases/phase-0/design/auth.md"
    assert html_path(docs, reader_path(docs, src)) == docs / "reader/html/phases/phase-0/design/auth.html"
