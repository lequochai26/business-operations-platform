"""Chụp file HTML (mockup, preview) thành PNG bằng Playwright.

Chạy: py tools/ui/screenshot.py <file-hoặc-thư-mục>... --out <thư-mục> [--viewport 1440x900]
Thư mục: chụp mọi *.html nằm trực tiếp trong đó.
"""

import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def capture(html_files: list[Path], out_dir: Path, viewport: tuple[int, int] = (1440, 900)) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    shots = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": viewport[0], "height": viewport[1]})
        for html in html_files:
            page.goto(html.resolve().as_uri())
            page.wait_for_load_state("networkidle")
            shot = out_dir / f"{html.stem}.png"
            page.screenshot(path=str(shot), full_page=True)
            shots.append(shot)
        browser.close()
    return shots


def _collect(paths: list[str]) -> list[Path]:
    files = []
    for raw in paths:
        path = Path(raw)
        files += sorted(path.glob("*.html")) if path.is_dir() else [path]
    return files


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Chụp HTML thành PNG")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--out", required=True)
    parser.add_argument("--viewport", default="1440x900")
    args = parser.parse_args(argv)
    width, height = (int(v) for v in args.viewport.lower().split("x"))
    files = _collect(args.paths)
    if not files:
        print("Không có file HTML nào để chụp")
        return 1
    for shot in capture(files, Path(args.out), (width, height)):
        print(f"Đã chụp {shot}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
