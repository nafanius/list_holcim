from datetime import time
import pytest
from statistic.order import Order

@pytest.fixture(scope="module")
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

class TestTelToString:

    def test_tel_to_string_with_float(self, order):
        # Test when input is a float
        result = order.tel_to_string(123456.0)
        assert result == "123456"

    def test_tel_to_string_with_int(self, order):
        # Test when input is a float
        result = order.convert_to_string(order.tel_to_string(123456))
        assert result == "123456"

    def test_tel_to_string_multi_tel(self, order):
        # Test when input is a float
        result = order.tel_to_string("123456 654321")
        assert result == "123456 654321"

    def test_tel_to_string_multi_tel_n(self, order):
        # Test when input is a float
        result = order.convert_to_string(order.tel_to_string("123456 \n  654321\n"))
        assert result == "123456 654321"

    def test_tel_to_string_multi_tel_t(self, order):
        # Test when input is a float
        result = order.convert_to_string(order.tel_to_string("123456 \t  654321\n"))
        assert result == "123456 654321"

    def test_tel_to_string_with_string(self, order):
        # Test when input is a string
        result = order.tel_to_string(" 123456 ")
        result_n = order.tel_to_string(" 123456\n")
        result_multi_n = order.tel_to_string("\n\n123456\n")
        result_t = order.tel_to_string("123456\t")
        result_multi_t = order.tel_to_string("\t123456\t")

        assert result == "123456"
        assert result_n == "123456"
        assert result_multi_n == "123456"
        assert result_t == "123456"
        assert result_multi_t == "123456"

    def test_tel_to_string_with_none(self, order):
        # Test when input is None
        result = order.tel_to_string(None)
        assert result == ""

    def test_tel_to_string_with_empty_string(self, order):
        # Test when input is an empty string
        result = order.tel_to_string("")
        assert result == ""

    def test_tel_to_string_with_invalid_type(self, order):
        # Test when input is an invalid type (e.g., list)
        result = order.tel_to_string(["123456"])
        assert result == ""

class TestGetListCourses:

    def test_get_list_courses_with_zero_metres(self, order):
        # Test when metres is 0
        order.metres = 0
        result = order.get_list_courses()
        assert result == [0]

    def test_get_list_courses_with_exact_division(self, order):
        # Test when metres is exactly divisible by 8
        order.metres = 16
        result = order.get_list_courses()
        assert result == [8.0, 8.0]

    def test_get_list_courses_with_remainder_less_than_2(self, order):
        # Test when remainder is less than 2
        order.metres = 17
        result = order.get_list_courses()
        assert result == [8.0, 7.0, 2.0]

    def test_get_list_courses_with_remainder_greater_than_or_equal_to_2(self, order):
        # Test when remainder is greater than or equal to 2
        order.metres = 18
        result = order.get_list_courses()
        assert result == [8.0, 8.0, 2.0]

    def test_get_list_courses_with_metres_less_than_8(self, order):
        # Test when metres is less than 8
        order.metres = 5
        result = order.get_list_courses()
        assert result == [5.0]

    def test_get_list_courses_with_formul_metrs(self, order):
        # Test when metres is less than 8
        order.metres = 5 + 10
        result = order.get_list_courses()
        assert result == [8.0, 7.0]
    
    def test_get_list_courses_with_less_1metr(self, order):
        # Test when metres less then 1m
        order.metres = 0.5
        result = order.get_list_courses()
    
    def test_get_list_courses_with_0_metrs(self, order):
        # Test when metres is less than 8
        order.metres = 0
        result = order.get_list_courses()
        assert result == [0.0]

class TestPompaDzwig:

    def test_empty_metrs(self, order):
        result = order.check_pompa_dzwig('501', 0)
        result1 = order.check_pompa_dzwig('', 0)
        result2 = order.check_pompa_dzwig(True, 0)
        result3 = order.check_pompa_dzwig(None, 0)
        result4 = order.check_pompa_dzwig(False, 0)
        result5 = order.check_pompa_dzwig(-5, 0)
        result6 = order.check_pompa_dzwig(1.2, 0)
        assert False == result
        assert False == result1
        assert True == result2
        assert False == result3
        assert False == result4
        assert True == result5
        assert True == result6

    def test_if_pompa_dzwig_empty(self, order):
        result = order.check_pompa_dzwig('', 10)
        assert False == result

    def test_if_pompa_dzwig_empty_and_metres_50(self, order):
        result = order.check_pompa_dzwig('', 50)
        assert False == result 
    def test_if_pompa_dzwig_empty_and_metres_more_50(self, order):
        result = order.check_pompa_dzwig('', 55)
        assert True == result 

    def test_if_pompa_dzwig_empty_and_metres_none(self, order):
        result = order.check_pompa_dzwig('', order.convert_to_float(None))
        assert False == result 

    def test_if_pompa_dzwig_empty_and_metres_true(self, order):
        result = order.check_pompa_dzwig('', True)
        assert False == result 
        
    def test_if_pompa_dzwig_empty_and_metres_false(self, order):
        result = order.check_pompa_dzwig('', False)
        assert False == result 

    def test_if_pompa_dzwig_empty_and_metres_negative(self, order):
        result = order.check_pompa_dzwig('', -10)
        assert False == result 

    def test_if_pompa_dzwig_empty_and_metres_string(self, order):
        result = order.check_pompa_dzwig('', order.convert_to_float('10'))
        assert False == result 



