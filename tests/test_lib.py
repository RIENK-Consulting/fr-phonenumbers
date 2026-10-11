from fr_phonenumbers import get_operator, parse_phone_number


def test_parse_phone_number():
    assert parse_phone_number("01 05 71 23 45") == 105712345
    assert parse_phone_number("+33105712345") == 105712345


def test_get_operator():
    res = get_operator("0105712345")
    assert res is not None
    assert res["code"] == "FRTE"
