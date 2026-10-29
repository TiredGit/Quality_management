import pytest

from src.currency import format_currency


def test_format_rubles():
    assert format_currency(100, "RUB") == "100.00 RUB"


def test_format_dollars():
    assert format_currency(12.5, "USD") == "12.50 USD"


def test_format_zero():
    assert format_currency(0, "EUR") == "0.00 EUR"


def test_round_to_two():
    assert format_currency(10.126, "EUR") == "10.13 EUR"


def test_unsupported_currency():
    with pytest.raises(ValueError, match="Unsupported currency"):
        format_currency(100, "TST")


def test_negative_amount():
    with pytest.raises(ValueError, match="non-negative"):
        format_currency(-10, "RUB")


def test_not_number():
    with pytest.raises(ValueError, match="must be a number"):
        format_currency(True, "RUB")
