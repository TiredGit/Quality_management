import re
from datetime import date as Date

from pydantic import BaseModel, ConfigDict, Field, field_validator

AVAILABLE_SERVICES = {
    "Мужская стрижка",
    "Стрижка машинкой",
    "Фейд",
    "Детская стрижка",
    "Моделирование бороды",
    "Королевское бритьё",
    "Бритьё головы",
    "Оформление усов",
    "Стрижка + борода",
    "Отец + сын",
    "Стрижка + бритьё",
    "VIP-комплекс",
}

AVAILABLE_BARBERS = {
    "any",
    "artem",
    "dmitry",
    "kirill",
    "roman",
}

AVAILABLE_TIMES = {
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
    "18:00",
    "19:00",
    "20:00",
}


class BookingRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,
    )

    name: str = Field(min_length=2, max_length=80)
    phone: str = Field(min_length=10, max_length=25)
    service: str
    barber: str = "any"
    booking_date: Date = Field(alias="date")
    time: str
    comment: str = Field(default="", max_length=500)
    agree: bool

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        if not re.fullmatch(r"[0-9+\-()\s]+", value):
            raise ValueError("Телефон содержит недопустимые символы")

        digits = re.sub(r"\D", "", value)

        if not 10 <= len(digits) <= 15:
            raise ValueError("Некорректная длина номера телефона")

        return value

    @field_validator("service")
    @classmethod
    def validate_service(cls, value: str) -> str:
        if value not in AVAILABLE_SERVICES:
            raise ValueError("Неизвестная услуга")

        return value

    @field_validator("barber")
    @classmethod
    def validate_barber(cls, value: str) -> str:
        if value not in AVAILABLE_BARBERS:
            raise ValueError("Неизвестный мастер")

        return value

    @field_validator("booking_date")
    @classmethod
    def validate_date(cls, value: Date) -> Date:
        if value < Date.today():
            raise ValueError("Нельзя выбрать дату в прошлом")

        return value

    @field_validator("time")
    @classmethod
    def validate_time(cls, value: str) -> str:
        if value not in AVAILABLE_TIMES:
            raise ValueError("Недоступное время записи")

        return value

    @field_validator("agree")
    @classmethod
    def validate_agreement(cls, value: bool) -> bool:
        if value is not True:
            raise ValueError("Необходимо согласие на обработку данных")

        return value
