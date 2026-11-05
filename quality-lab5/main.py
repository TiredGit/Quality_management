from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.booking import BookingRequest

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


@app.post("/api/bookings")
def create_booking(booking: BookingRequest) -> dict[str, str]:
    return {"message": ("Данные формы успешно проверены сервером. ")}


app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
