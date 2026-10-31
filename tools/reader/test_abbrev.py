from reader.abbrev import definition_lines, expand_abbreviations, parse_abbreviations

DEFS = """## Ghi chú chạy

- Viết tắt trong các bước:
  - `<api>` = `http://127.0.0.1:3000/api/v1`;
  - `<psql> "<sql>"` = `docker compose exec -T postgres psql -U mio -d mio -c "<sql>"`;
  - `<origin>` = `-H 'Origin: http://localhost:3000'`; `<json>` = `-H 'Content-Type: application/json'`;
  - `<đăng nhập mio>` = `curl -s -i -c mio.jar <origin> <json> <api>/sessions`;
"""


def test_simple_abbreviation():
    abbrevs = parse_abbreviations(DEFS)
    assert expand_abbreviations("Gọi `<api>/sessions`.", abbrevs) == "Gọi `http://127.0.0.1:3000/api/v1/sessions`."


def test_parametric_abbreviation():
    abbrevs = parse_abbreviations(DEFS)
    assert (
        expand_abbreviations('Chạy `<psql> "delete from user_sessions"`.', abbrevs)
        == 'Chạy `docker compose exec -T postgres psql -U mio -d mio -c "delete from user_sessions"`.'
    )


def test_nested_abbreviation():
    abbrevs = parse_abbreviations(DEFS)
    assert expand_abbreviations("`<đăng nhập mio>`", abbrevs) == (
        "`curl -s -i -c mio.jar -H 'Origin: http://localhost:3000' -H 'Content-Type: application/json' "
        "http://127.0.0.1:3000/api/v1/sessions`"
    )


def test_trailing_parameter_takes_rest_of_code_span():
    abbrevs = parse_abbreviations("- `<x> <a>` = `run <a> now`;\n")
    assert expand_abbreviations("Chạy `<x> foo bar`.", abbrevs) == "Chạy `run foo bar now`."


def test_two_definitions_on_one_line():
    names = [a.name for a in parse_abbreviations(DEFS)]
    assert names == ["<api>", "<psql>", "<origin>", "<json>", "<đăng nhập mio>"]


def test_unknown_abbreviation_left_as_is():
    abbrevs = parse_abbreviations(DEFS)
    assert expand_abbreviations("Thử lại sau <n> phút, `<cli> list-users`", abbrevs) == "Thử lại sau <n> phút, `<cli> list-users`"


def test_definition_lines():
    assert definition_lines(DEFS) == {4, 5, 6, 7}
