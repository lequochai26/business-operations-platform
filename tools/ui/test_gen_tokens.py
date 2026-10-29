import pytest

from gen_tokens import HEADER, extract_tokens, tokens_to_css


def test_tokens_to_css_nested():
    css = tokens_to_css({"color": {"primary": "#8FA284", "surface": {"card": "#FAF7F0"}}})
    assert "--color-primary: #8FA284;" in css
    assert "--color-surface-card: #FAF7F0;" in css


def test_tokens_to_css_header():
    css = tokens_to_css({"radius": {"md": "8px"}})
    assert css.splitlines()[0] == HEADER
    assert HEADER == "/* File sinh tự động từ ui-style.md, không sửa tay. */"
    assert ":root {" in css


def test_extract_tokens_reads_block_under_heading():
    md = (
        "# Style\n\n```yaml\nkhac: 1\n```\n\n"
        "## Tokens\n\nMô tả.\n\n```yaml\ncolor:\n  primary: '#8FA284'\n```\n\n## Typography\n"
    )
    assert extract_tokens(md) == {"color": {"primary": "#8FA284"}}


def test_extract_tokens_missing_block():
    with pytest.raises(ValueError, match="## Tokens"):
        extract_tokens("# Style\n\n## Typography\n")
