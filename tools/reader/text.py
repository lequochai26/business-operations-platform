"""Đọc và chuẩn hóa văn bản dùng chung cho các bước sinh bản đọc."""

import hashlib
import re
import unicodedata
from pathlib import Path


def clean(text: str) -> str:
    """Bỏ BOM, đổi CRLF thành LF, chuẩn hóa NFC."""
    return unicodedata.normalize("NFC", text.lstrip("﻿").replace("\r\n", "\n"))


def read_text(path: Path) -> str:
    return clean(path.read_text(encoding="utf-8"))


def normalize(s: str) -> str:
    """Dạng so sánh: NFC, gộp mọi khoảng trắng thành một dấu cách."""
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s)).strip()


def short_hash(s: str, n: int = 12) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:n]
