from PIL import Image

from screenshot import capture


def write_html(path, body):
    path.write_text(f"<!doctype html><meta charset='utf-8'><body style='margin:0'>{body}</body>", encoding="utf-8")


def test_capture_uses_viewport_width(tmp_path):
    html = tmp_path / "normal.html"
    write_html(html, "<div style='height:100px;background:#8FA284'></div>")
    shots = capture([html], tmp_path / "shots")
    assert shots == [tmp_path / "shots" / "normal.png"]
    with Image.open(shots[0]) as img:
        assert img.width == 1440


def test_capture_renders_vietnamese(tmp_path):
    html = tmp_path / "vi.html"
    write_html(html, "<h1>Mẫu mới đón 20/10</h1>")
    shots = capture([html], tmp_path / "shots", viewport=(390, 844))
    with Image.open(shots[0]) as img:
        assert img.width == 390
