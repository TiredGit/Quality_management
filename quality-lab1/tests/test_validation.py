import pytest

from src.validation import validate_email


@pytest.mark.parametrize(
    "email",
    [
        "user@example.com",
        "student.name@university.edu",
        "user+test@example.org",
        "user@sub.example.com",
    ],
)
def test_valid_emails(email):
    assert validate_email(email) is True


@pytest.mark.parametrize(
    "email",
    [
        "",
        "plain-text",
        "user@",
        "@example.com",
        "user name@example.com",
        "user@example..com",
    ],
)
def test_invalid_emails(email):
    assert validate_email(email) is False


@pytest.mark.parametrize("email", [None, 123, [], True])
def test_non_string_values_are_invalid(email):
    assert validate_email(email) is False
