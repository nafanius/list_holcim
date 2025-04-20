from datetime import time
import datetime
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

    @pytest.mark.parametrize(
            "string",
            ["123456 \n  654321\n",
             "123456 \t  654321\n",
             "123456 \t       654321\n",
             "123456 654321\n",
             "\n\n\n\n123456 \t654321\n"]
    )
    def test_tel_to_string_multi_tel_n(self, order, string):
        # Test when input is a float
        result = order.convert_to_string(order.tel_to_string(string))
        assert result == "123456 654321"

    @pytest.mark.parametrize(
            "string",
            [" 123456 \n",
             "123456 \t",
             "\t\n123456 \t",
             "  \n 123456   \n",
             "\n\n\t\n\n123456 \t"]
    )
    def test_tel_to_string_with_string(self, order, string):
        # Test when input is a string
        result = order.convert_to_string(order.tel_to_string(string))
        assert result == "123456"
       
    @pytest.mark.parametrize(
            "string",
            ["",
             None,
             [],
             {},
             (),
             ["123456"],
             ("1225ddf2214",),
             0,
             0000]
    )
    def test_tel_to_string_with_none_and_invalid_type(self, order, string):
        # Test when input is None
        result = order.convert_to_string(order.tel_to_string(string))
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
        assert result == [0.5]
    
    def test_get_list_courses_with_0_metrs(self, order):
        # Test when metres is less than 8
        order.metres = 0
        result = order.get_list_courses()
        assert result == [0.0]

class TestPompaDzwig:

    @pytest.mark.parametrize(
            "pomp",
            [True,
             -5,
              1.2,
             "pompa",
             "ivanof",
             (1,),
             [1],
             {1:"one"}
             ]
    )
    def test_empty_metrs_true(self, order, pomp):
        result = order.check_pompa_dzwig(pomp, 0)
    
        assert True == result

    @pytest.mark.parametrize(
            "pomp",
            [0,
             "",
             None,
             "501",
             {},
             [],
             ()
             ]
    )
    def test_empty_metrs_false(self, order, pomp):
        result = order.check_pompa_dzwig(pomp, 0)
        assert False == result

    @pytest.mark.parametrize(
            "m",
            [0,
             10,
             None,
             50,
             {},
             [],
             "",
             False,
             True,
             -10,
             -50,
             -60]
    )
    def test_if_pompa_dzwig_empty(self, order, m):
        order.metres = order.convert_to_float(m)
        metrs_from_order = order.metres
        result = order.check_pompa_dzwig('', metrs_from_order)
        assert False == result
  
    @pytest.mark.parametrize(
            "m",
            [51,
             50.005,
             60,
             158.3,
             50.1]
    )
    def test_if_pompa_dzwig_empty_and_metres_more_50(self, order, m):
        order.metres = order.convert_to_float(m)
        metrs_from_order = order.metres
        result = order.check_pompa_dzwig('', metrs_from_order)
        assert True == result

class TestGetStartTime:

    def test_get_start_time(self, order):
        result = order.get_start_time()
        assert result == datetime.datetime(2025, 1, 1, 9, 40)

    def test_get_start_time_00(self, order):
        order.times = time(hour=0, minute=0)
        result = order.get_start_time()
        assert result == datetime.datetime(2024, 12, 31, 23, 30)
