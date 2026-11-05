from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def valid_booking_data() -> dict:
    return {
        "name": "Иван",
        "phone": "+7 900 000-00-00",
        "service": "Мужская стрижка",
        "barber": "artem",
        "date": (date.today() + timedelta(days=2)).isoformat(),
        "time": "12:00",
        "comment": "Без дополнительных пожеланий",
        "agree": True,
    }


@pytest.fixture
def api_client():
    with TestClient(app) as client:
        yield client
