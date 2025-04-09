from datetime import time
import pytest
from statistic.order import Order

@pytest.fixture
def order():
    # Create a dummy Order instance for testing
    return Order(
        date_order="01.01.2025",
        metres=0,
        times=time(hour=10, minute=10),
        firm="Test Firm",
        name="Test Name",
        uwagi="Test Uwagi",
        przebieg="Test Przebieg",
        tel="123456789",
        wenz=1,
        pompa_dzwig="pompa"
    )


def test_count_order():
    o1 = Order(
        date_order="01.01.2025",
        metres=0,
        times=time(hour=10, minute=10),
        firm="Test Firm",
        name="Test Name",
        uwagi="Test Uwagi",
        przebieg="Test Przebieg",
        tel="123456789",
        wenz=1,
        pompa_dzwig="pompa"
    )
    o2 = Order(
        date_order="01.01.2025",
        metres=0,
        times=time(hour=10, minute=20),
        firm="Test Firm",
        name="Test Name2",
        uwagi="Test Uwagi",
        przebieg="Test Przebieg",
        tel="123456789",
        wenz=1,
        pompa_dzwig="pompa"
    )
    o3 = Order(
        date_order="01.01.2025",
        metres=0,
        times=time(hour=10, minute=30),
        firm="Test Firm",
        name="Test Name3",
        uwagi="Test Uwagi",
        przebieg="Test Przebieg",
        tel="123456789",
        wenz=1,
        pompa_dzwig="pompa"
    )
    o4 = Order(
        date_order="01.01.2025",
        metres=0,
        times=time(hour=10, minute=40),
        firm="Test Firm",
        name="Test Name4",
        uwagi="Test Uwagi",
        przebieg="Test Przebieg",
        tel="123456789",
        wenz=1,
        pompa_dzwig="pompa"
    )
    assert o4.count_ordres == 4

# region tel_to_string
def test_tel_to_string_with_float(order):
    # Test when input is a float
    result = order.tel_to_string(123456.0)
    assert result == "123456"

def test_tel_to_string_with_string(order):
    # Test when input is a string
    result = order.tel_to_string(" 123456 ")
    assert result == "123456"

def test_tel_to_string_with_none(order):
    # Test when input is None
    result = order.tel_to_string(None)
    assert result == ""

def test_tel_to_string_with_empty_string(order):
    # Test when input is an empty string
    result = order.tel_to_string("")
    assert result == ""

def test_tel_to_string_with_invalid_type(order):
    # Test when input is an invalid type (e.g., list)
    result = order.tel_to_string(["123456"])
    assert result == ""
# endregion

# region test get_list_courses
def test_get_list_courses_with_zero_metres(order):
    # Test when metres is 0
    order.metres = 0
    result = order.get_list_courses()
    assert result == [0]

def test_get_list_courses_with_exact_division(order):
    # Test when metres is exactly divisible by 8
    order.metres = 16
    result = order.get_list_courses()
    assert result == [8.0, 8.0]

def test_get_list_courses_with_remainder_less_than_2(order):
    # Test when remainder is less than 2
    order.metres = 17
    result = order.get_list_courses()
    assert result == [8.0, 7.0, 2.0]

def test_get_list_courses_with_remainder_greater_than_or_equal_to_2(order):
    # Test when remainder is greater than or equal to 2
    order.metres = 18
    result = order.get_list_courses()
    assert result == [8.0, 8.0, 2.0]

def test_get_list_courses_with_metres_less_than_8(order):
    # Test when metres is less than 8
    order.metres = 5
    result = order.get_list_courses()
    assert result == [5.0]
# endregion

