import pytest

from cr_pr import format_price, price_direction


@pytest.mark.parametrize(("price", "expected"), [
    (81501, "81501.00"),
    (2385.876, "2385.88"),
    (1, "1.00"),
    (0.00000417, "0.00000417"),
    (0.5, "0.50000000"),
    ("N/A", "N/A"),
    (None, "N/A"),
])
def test_format_price(price, expected):
    assert format_price(price) == expected


@pytest.mark.parametrize(("price", "previous", "expected"), [
    (2.0, 1.0, "↑"),
    (1.0, 2.0, "↓"),
    (1.0, 1.0, "-"),
    (1.0, None, "-"),   # first fetch, no previous price
    ("N/A", 1.0, "-"),  # coin missing from the API response
    (1.0, "N/A", "-"),
])
def test_price_direction(price, previous, expected):
    assert price_direction(price, previous) == expected
