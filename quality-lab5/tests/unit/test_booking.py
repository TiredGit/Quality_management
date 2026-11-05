from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from src.booking import BookingRequest


def test_valid_booking(valid_booking_data):
    booking = BookingRequest.model_validate(valid_booking_data)

    assert booking.name == "Иван"
    assert booking.service == "Мужская стрижка"
    assert booking.barber == "artem"
    assert booking.agree is False


def test_name_whitespace_is_removed(valid_booking_data):
    valid_booking_data["name"] = "  Иван  "

    booking = BookingRequest.model_validate(valid_booking_data)

    assert booking.name == "Иван"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("phone", "123"),
        ("service", "Несуществующая услуга"),
        ("barber", "unknown"),
        ("date", (date.today() - timedelta(days=1)).isoformat()),
        ("time", "09:00"),
        ("agree", False),
    ],
)
def test_invalid_booking_data(valid_booking_data, field, value):
    valid_booking_data[field] = value

    with pytest.raises(ValidationError):
        BookingRequest.model_validate(valid_booking_data)


def test_empty_name_is_rejected(valid_booking_data):
    valid_booking_data["name"] = ""

    with pytest.raises(ValidationError):
        BookingRequest.model_validate(valid_booking_data)


def test_long_comment_is_rejected(valid_booking_data):
    valid_booking_data["comment"] = "А" * 501

    with pytest.raises(ValidationError):
        BookingRequest.model_validate(valid_booking_data)
