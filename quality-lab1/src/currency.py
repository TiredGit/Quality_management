def format_currency(amount: float, currency: str) -> str:
    if currency not in {"RUB", "USD", "EUR"}:
        raise ValueError("Unsupported currency")

    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise ValueError("Amount must be a number")

    if amount < 0:
        raise ValueError("Amount must be non-negative")
    return f"{amount:.2f} {currency}"
