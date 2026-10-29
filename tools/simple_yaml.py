"""Parser YAML tối giản: mapping lồng nhau (thụt lề bằng dấu cách) và giá trị chuỗi.

Dùng thay PyYAML (chưa có bản cho Python 3.15). Đủ cho frontmatter của skill và khối tokens.
"""


def _strip_comment(value: str) -> str:
    quote = None
    for i, ch in enumerate(value):
        if ch in "'\"" and quote is None:
            quote = ch
        elif ch == quote:
            quote = None
        elif ch == "#" and quote is None and (i == 0 or value[i - 1] in " \t"):
            return value[:i]
    return value


def _scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    return value


def parse(text: str) -> dict:
    root: dict = {}
    # Mỗi frame: [thụt lề của các khóa (None = chưa biết), mapping, thụt lề của khóa cha]
    frames: list[list] = [[0, root, -1]]
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = _strip_comment(raw).rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        while True:
            top = frames[-1]
            if top[0] is None:
                if indent > top[2]:
                    top[0] = indent
                    break
                frames.pop()
                continue
            if indent == top[0]:
                break
            if indent < top[0] and len(frames) > 1:
                frames.pop()
                continue
            raise ValueError(f"Thụt lề sai ở dòng {lineno}: {raw!r}")
        key, sep, rest = line.strip().partition(":")
        if not sep or not key.strip():
            raise ValueError(f"YAML không hợp lệ ở dòng {lineno}: {raw!r}")
        if rest.strip():
            frames[-1][1][key.strip()] = _scalar(rest)
        else:
            child: dict = {}
            frames[-1][1][key.strip()] = child
            frames.append([None, child, indent])
    return root
