def calculate_total(items):
    if not isinstance(items, list):
        raise ValueError("Items must be an array")

    total = 0

    for item in items:
        price = item["price"]

        if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Invalid price")

        total += price * (item.get("quantity") or 1)

    return total


def apply_discount(total, discount_percent):
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")

    return total * (1 - discount_percent / 100)
