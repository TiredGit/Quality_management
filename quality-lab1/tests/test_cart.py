import pytest

from src.cart import apply_discount, calculate_total


class TestCalculateTotal:
    def test_return_zero_for_empty_list(self):
        assert calculate_total([]) == 0

    def test_sum_prices_correctly(self):
        items = [
            {"price": 100, "quantity": 2},
            {"price": 50, "quantity": 1},
        ]
        assert calculate_total(items) == 250

    def test_raise_error_for_non_list(self):
        with pytest.raises(ValueError, match="Items must be an array"):
            calculate_total("invalid")

    def test_raise_error_for_negative_price(self):
        items = [{"price": -10}]
        with pytest.raises(ValueError, match="Invalid price"):
            calculate_total(items)


class TestApplyDiscount:
    def test_apply_ten_percent_discount(self):
        assert apply_discount(100, 10) == 90

    def test_raise_error_for_discount_over_100(self):
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            apply_discount(100, 150)
