from datetime import time
import datetime
import pytest
from statistic.order import Order
from src.settings import inf
from src.settings import Settings
import re


@pytest.fixture(scope="class")
def order():
    # Create a dummy Order instance for testing
    order_obj =  Order(
        date_order = "01.01.2025",
        metres = 0,
        times = time(hour=10, minute=10),
        firm = "Test Firm",
        name = "Test Name",
        uwagi = "Test Uwagi",
        przebieg = "Test Przebieg",
        tel = "123456789",
        wenz = 1,
        pompa_dzwig = True 
    )

    yield order_obj

    del order_obj
    

class TestClassOrder:
    def test_count_order(self):
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
        del o1, o2, o3, o4

    def test_how_many(self):
        o5 = Order(
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
        assert o5.how_many() == "We have 5 orders."

class TestMetresToFloat:

    @pytest.mark.parametrize(("m3","response"),
                             [(0.5, 0.5),
                              (1.2, 1.2),
                              (8.115651515, 8.1),
                              (-12.0, 12.0),
                              (-0.0, 0.0),
                              (0.00000, 0.0),
                              (0.56, 0.6),
                              (0.45, 0.5),
                              (-0.45, 0.5),
                              (0.000004, 0.0)]
    )
    def test_float(self, order, m3, response):
        result = order.convert_to_float(m3)
        assert result == response


    @pytest.mark.parametrize(("m3","response"),
                             [(1, 1.0),
                              (150, 150.0),
                              (-1, 1.0),
                              (0, 0.0),
                              (-0.0, 0.0),
                              (-250, 250.0)]
    )
    def test_float_from_int(self, order, m3, response):
        result = order.convert_to_float(m3)
        assert result == response
    
    @pytest.mark.parametrize(("m3","response"),
                             [("1", 0.0),
                              (time, 0.0),
                              (object, 0.0),
                              ([1,], 0.0),
                              ({}, 0.0),
                              ((1,), 0.0),
                              (None, 0.0),
                              (0, 0.0),
                              ("", 0.0),
                              ({"1":1}, 0.0)]
    )
    def test_float_not_flot_or_int(self, order, m3, response):
        result = order.convert_to_float(m3)
        assert result == response

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
            ("pomp", "m", "response"),
            [(True, -10, True), 
             ('501',10, False),
             ('P-2 Olszewski pompogruszka bierze beton zał g  g 13:10',10, True),
             ('Niziński ',100, True),
             ('501',-100, False),
             ('501',50, False),
            ]
    )
    def test_have_501(self, order, pomp, m, response):
        result = order.check_pompa_dzwig(pomp, m)
        assert response == result


    @pytest.mark.parametrize(
            ("pomp", "m", "response","cancel"),
            [(True, -10, True, False), 
             ('501',10, False, False),
             ('P-2 Olszewski pompogruszka bierze beton zał g  g 13:10', 5.5, True, True),
             ('P-2 Olszewski pompogruszka bierze beton zał g  g 13:10', 6, True, False),
             ('pompogruszka bierze beton zał g  g 13:10', 30, True, False),
             ('P-2 Olszewski pompogruszka bierze beton zał g  g 13:10', 4, True, True),
             ('mpogruszka bierze beton zał g  g 13:10', 4, True, False),
             ('P-2 Olszewski pompogruszka bierze beton zał g  g 13:10', 1, True, True),
             ('P-28 Olszewski Pompogruszka bierze beton zał g 7:00 + plus węże 6mb i 6mb', 2, True, True),
             ('Niziński ',100, True, False),
             ('501',-100, False, False),
             ('501',50, False, False),
            ]
    )
    def test_have_pompogruszka(self, order, pomp, m, response, cancel):
        order.cancellation = False
        result_pomp = order.check_pompa_dzwig(pomp, m)
        result_cancellation = order.cancellation
        assert (response, cancel) == (result_pomp, result_cancellation)

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
             -50]
    )
    def test_if_pompa_dzwig_empty(self, order, m):
        order.metres = order.convert_to_float(m)
        metrs_from_order = order.metres
        result = order.check_pompa_dzwig('', metrs_from_order)
        assert False == result
  
    @pytest.mark.parametrize(
            "m",
            [51,
             50.1,
             60,
             158.3,
             -60]
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

    @pytest.mark.parametrize(("set_times", "set_date", "response"),
            [(time(hour=10, minute=10), "01.10.2024", datetime.datetime(2024, 10, 1, 9, 40)),
             (time(hour=5, minute=10), "01.10.2024", datetime.datetime(2024, 10, 1, 4, 40)),
             (time(hour=10, minute=0), "01.10.2024", datetime.datetime(2024, 10, 1, 9, 30)),
             (time(hour=10, minute=10), "02.10.2025", datetime.datetime(2025, 10, 2, 9, 40)),
             (time(hour=10, minute=10), "01.09.2024", datetime.datetime(2024, 9, 1, 9, 40)),
             (time(hour=0, minute=0), "01.01.2024", datetime.datetime(2023, 12, 31, 23, 30))]
    )
    def test_get_start_time_change_data_order(self, order, set_times, set_date, response):
        order.times = set_times
        order.date_order = set_date
        result = order.get_start_time()
        assert result == response

class TestGetFinishTime:

    @pytest.mark.parametrize(("set_times", "set_date", "m3",  "response"),
            [(time(hour=10, minute=10), "01.10.2024", 18.0, datetime.datetime(2024, 10, 1, 10, 12)),
             (time(hour=5, minute=10), "01.10.2024", 100.0, datetime.datetime(2024, 10, 1, 7, 52)),
             (time(hour=10, minute=0), "01.10.2024", 8.0, datetime.datetime(2024, 10, 1, 9, 30)),
             (time(hour=10, minute=0), "01.10.2024", 8.1, datetime.datetime(2024, 10, 1, 9, 44)),
             (time(hour=10, minute=10), "02.10.2025", 25.0, datetime.datetime(2025, 10, 2, 10, 26)),
             (time(hour=10, minute=10), "01.09.2024", 12.0, datetime.datetime(2024, 9, 1, 9, 56)),
             (time(hour=0, minute=0), "01.01.2024", 45.0, datetime.datetime(2024, 1, 1, 0, 50))]
    )
    def test_finish_for_pomp(self, order, set_times, set_date, m3, response):
        """this test will be fail if Settings.unloading_time_for_pomp changed
        """        
        order.times = set_times
        order.date_order = set_date
        order.metres = m3
        order.list_of_courses = order.get_list_courses()
        order.start_time = order.get_start_time()
        result = order.get_finish_time_and_form_list_times_of_loads()
        assert result == response

    @pytest.mark.parametrize(("set_times", "set_date", "m3",  "response"),
            [(time(hour=10, minute=10), "01.10.2024", 18.0, datetime.datetime(2024, 10, 1, 11, 3, 12)),
             (time(hour=5, minute=10), "01.10.2024", 2.0, datetime.datetime(2024, 10, 1, 4, 40)),
             (time(hour=10, minute=0), "01.10.2024", 8.0, datetime.datetime(2024, 10, 1, 9, 30)),
             (time(hour=10, minute=0), "01.10.2024", 8.1, datetime.datetime(2024, 10, 1, 10, 6, 24)),
             (time(hour=10, minute=10), "02.10.2025", 25.0, datetime.datetime(2025, 10, 2, 11, 39, 36)),
             (time(hour=10, minute=10), "01.09.2024", 16.6, datetime.datetime(2024, 9, 1, 10, 58)),
             (time(hour=0, minute=0), "01.01.2024", 45.0, datetime.datetime(2024, 1, 1, 2, 58))]
    )
    def test_finish_for_dzwig(self, order, set_times, set_date, m3, response):
        """this test will be fail if Settings.unloading_time_for_crane changed
        """  
        order.pompa_dzwig = False
        order.times = set_times
        order.date_order = set_date
        order.metres = m3
        order.list_of_courses = order.get_list_courses()
        order.start_time = order.get_start_time()
        result = order.get_finish_time_and_form_list_times_of_loads()
        assert result == response

class TestGetListOfTimeLoads:

    @pytest.mark.parametrize(("set_times", "set_date", "m3",  "response"),
            [(time(hour=10, minute=10), "01.10.2024", 18.0, [datetime.datetime(2024, 10, 1, 9, 40),
                                                             datetime.datetime(2024, 10, 1, 9, 56),
                                                             datetime.datetime(2024, 10, 1, 10, 12)]),
             (time(hour=5, minute=10), "01.10.2024", 100.0, [datetime.datetime(2024, 10, 1, 4, 40),
                                                             datetime.datetime(2024, 10, 1, 4, 56),
                                                             datetime.datetime(2024, 10, 1, 5, 12),
                                                             datetime.datetime(2024, 10, 1, 5, 28),
                                                             datetime.datetime(2024, 10, 1, 5, 44),
                                                             datetime.datetime(2024, 10, 1, 6, 0),
                                                             datetime.datetime(2024, 10, 1, 6, 16),
                                                             datetime.datetime(2024, 10, 1, 6, 32),
                                                             datetime.datetime(2024, 10, 1, 6, 48),
                                                             datetime.datetime(2024, 10, 1, 7, 4),
                                                             datetime.datetime(2024, 10, 1, 7, 20),
                                                             datetime.datetime(2024, 10, 1, 7, 36),
                                                             datetime.datetime(2024, 10, 1, 7, 52)]),
             (time(hour=10, minute=0), "01.10.2024", 8.0, [datetime.datetime(2024, 10, 1, 9, 30)]),
             (time(hour=10, minute=0), "01.10.2024", 8.1, [datetime.datetime(2024, 10, 1, 9, 30),
                                                           datetime.datetime(2024, 10, 1, 9, 44)]),
             (time(hour=10, minute=10), "02.10.2025", 25.0, [datetime.datetime(2025, 10, 2, 9, 40),
                                                             datetime.datetime(2025, 10, 2, 9, 56),
                                                             datetime.datetime(2025, 10, 2, 10, 12),
                                                             datetime.datetime(2025, 10, 2, 10, 26)]),
             (time(hour=10, minute=10), "01.09.2024", 12.0, [datetime.datetime(2024, 9, 1, 9, 40),
                                                             datetime.datetime(2024, 9, 1, 9, 56)]),
             (time(hour=10, minute=10), "01.09.2024", 0.0, []),
             (time(hour=0, minute=0), "01.01.2024", 50.0, [datetime.datetime(2023, 12, 31, 23, 30),
                                                           datetime.datetime(2023, 12, 31, 23, 46),
                                                           datetime.datetime(2024, 1, 1, 0, 2),
                                                           datetime.datetime(2024, 1, 1, 0, 18),
                                                           datetime.datetime(2024, 1, 1, 0, 34),
                                                           datetime.datetime(2024, 1, 1, 0, 50),
                                                           datetime.datetime(2024, 1, 1, 1, 6)])]
    )
    def test_form_list_of_load_pomp(self, order, set_times, set_date, m3, response):
        """this test will be fail if Settings.unloading_time_for_pomp changed
        """        
        order.times = set_times
        order.pompa_dzwig = True
        order.date_order = set_date
        order.metres = m3
        order.list_of_courses = order.get_list_courses()
        order.start_time = order.get_start_time()
        order.list_of_loads = []
        order.get_finish_time_and_form_list_times_of_loads()
        result = order.list_of_loads
        inf(result)
        assert result == response

    @pytest.mark.parametrize(("set_times", "set_date", "m3",  "response"),
            [(time(hour=10, minute=10), "01.10.2024", 18.0, [datetime.datetime(2024, 10, 1, 9, 40),
                                                             datetime.datetime(2024, 10, 1, 10, 21, 36),
                                                             datetime.datetime(2024, 10, 1, 11, 3, 12)]),
             (time(hour=5, minute=10), "01.10.2024", 100.0, [datetime.datetime(2024, 10, 1, 4, 40),
                                                             datetime.datetime(2024, 10, 1, 5, 21, 36),
                                                             datetime.datetime(2024, 10, 1, 6, 3, 12),
                                                             datetime.datetime(2024, 10, 1, 6, 44, 48),
                                                             datetime.datetime(2024, 10, 1, 7, 26, 24),
                                                             datetime.datetime(2024, 10, 1, 8, 8),
                                                             datetime.datetime(2024, 10, 1, 8, 49, 36),
                                                             datetime.datetime(2024, 10, 1, 9, 31, 12),
                                                             datetime.datetime(2024, 10, 1, 10, 12, 48),
                                                             datetime.datetime(2024, 10, 1, 10, 54, 24),
                                                             datetime.datetime(2024, 10, 1, 11, 36),
                                                             datetime.datetime(2024, 10, 1, 12, 17, 36),
                                                             datetime.datetime(2024, 10, 1, 12, 59, 12)]),
             (time(hour=10, minute=0), "01.10.2024", 8.0, [datetime.datetime(2024, 10, 1, 9, 30)]),
             (time(hour=10, minute=0), "01.10.2024", 8.1, [datetime.datetime(2024, 10, 1, 9, 30),
                                                           datetime.datetime(2024, 10, 1, 10, 6, 24)]),
             (time(hour=10, minute=10), "02.10.2025", 25.0, [datetime.datetime(2025, 10, 2, 9, 40),
                                                             datetime.datetime(2025, 10, 2, 10, 21, 36),
                                                             datetime.datetime(2025, 10, 2, 11, 3, 12),
                                                             datetime.datetime(2025, 10, 2, 11, 39, 36)]),
             (time(hour=10, minute=10), "01.09.2024", 12.0, [datetime.datetime(2024, 9, 1, 9, 40),
                                                             datetime.datetime(2024, 9, 1, 10, 21, 36)]),
             (time(hour=10, minute=10), "01.09.2024", 0.0, []),
             (time(hour=0, minute=0), "01.01.2024", 50.0, [datetime.datetime(2023, 12, 31, 23, 30),
                                                           datetime.datetime(2024, 1, 1, 0, 11, 36),
                                                           datetime.datetime(2024, 1, 1, 0, 53, 12),
                                                           datetime.datetime(2024, 1, 1, 1, 34, 48),
                                                           datetime.datetime(2024, 1, 1, 2, 16, 24),
                                                           datetime.datetime(2024, 1, 1, 2, 58),
                                                           datetime.datetime(2024, 1, 1, 3, 39, 36)])]
    )
    def test_form_list_of_load_dzwig(self, order, set_times, set_date, m3, response):
        """this test will be fail if Settings.unloading_time_for_pomp changed
        """        
        order.times = set_times
        order.pompa_dzwig = False
        order.date_order = set_date
        order.metres = m3
        order.list_of_courses = order.get_list_courses()
        order.start_time = order.get_start_time()
        order.list_of_loads = []
        order.get_finish_time_and_form_list_times_of_loads()
        result = order.list_of_loads
        inf(result)
        assert result == response

class TestGetConcellation:

    @pytest.mark.parametrize("pszebieg",
            ["kjkksk kdjjd odwołano sdkkkksdk",
            "odwołano 12.3.44",
            "gsgsg sggs odwołano",
            "odwołano 12.3.44"]
    )
    def test_consellation_in_przebeg_true(self, order, pszebieg):
        order.przebieg = pszebieg
        result  = order.get_cancellation()
        assert result == True

    @pytest.mark.parametrize("pszebieg",
            ["kjkksk kdjjd oddwocłano sdkkkksdk",
            "oddwołano 12.3.44",
            "gsgsg sggs odxwosłano",
            "odwxxołano 12.3.44"]
    )
    def test_consellation_in_przebeg_false(self, order, pszebieg):
        order.przebieg = pszebieg
        result  = order.get_cancellation()
        assert result == False

    @pytest.mark.parametrize(("pszebieg", "uwagi"),
            [("kjkksk kdjjd odwołano sdkkkksdk", "qqqw wq  sds vfvd ds"),
             ("odwołano 12.3.44", "qqqw wq  sds vfvd ds"),
             ("gsgsg sggs odwołano", "qqqw wq  sds vfvd ds"),
             ("odwołano 12.3.44", "qqqw wq  sds vfvd ds")]
    )
    def test_consellation_in_przebeg_uwagi_true(self, order, pszebieg, uwagi):
        order.przebieg = pszebieg
        order.uwagi = uwagi
        result  = order.get_cancellation()
        assert result == True
    
    @pytest.mark.parametrize(("pszebieg", "uwagi"),
            [("kjkksk kdjjd odwrosłano sdkkkksdk", "qqqw wq  sds vfvd ds"),
             ("odwsołano 12.3.44", "qqqw wq  sds vfvd ds"),
             ("gsgsg sggs odfwołano", "qqqw wq  sds vfvd ds"),
             ("odswołano 12.3.44", "qqqw wq  sds vfvd ds")]
    )
    def test_consellation_in_przebeg_uwagi_false(self, order, pszebieg, uwagi):
        order.przebieg = pszebieg
        order.uwagi = uwagi
        result  = order.get_cancellation()
        assert result == False

    @pytest.mark.parametrize(("uwagi", "pszebieg"),
            [("kjkksk kdjjd odwołano sdkkkksdk", "qqqw wq  sds vfvd ds"),
             ("odwołano 12.3.44", "qqqw wq  sds vfvd ds"),
             ("gsgsg sggs odwołano", "qqqw wq  sds vfvd ds"),
             ("", "sgsg sggs odwołanoqqqw wq  sds vfvd ds"),
             ("gsgsg sggs odwołano", ""),
             ("odwołano 12.3.44", "qqqw wq  sds vfvd ds")]
    )
    def test_consellation_in_uwagi_przebeg_true(self, order, pszebieg, uwagi):
        order.przebieg = pszebieg
        order.uwagi = uwagi
        result  = order.get_cancellation()
        assert result == True
    
    @pytest.mark.parametrize(("uwagi", "pszebieg"),
            [("kjkksk kdjjd odwrosłano sdkkkksdk", "qqqw wq  sds vfvd ds"),
             ("odwsołano 12.3.44", "qqqw wq  sds vfvd ds"),
             ("gsgsg sggs odfwołano", "qqqw wq  sds vfvd ds"),
             ("gsgsg sggs odfwołano", ""),
             ("", ""),
             ("", "gsgsg sggs odfwołano"),
             ("odswołano 12.3.44", "qqqw wq  sds vfvd ds")]
    )
    def test_consellation_in_uwagi_przebeg_false(self, order, pszebieg, uwagi):
        order.przebieg = pszebieg
        order.uwagi = uwagi
        result  = order.get_cancellation()
        assert result == False

class TestGetCheckZaprawa:

    @pytest.mark.parametrize(("list_of_courses","times", "name", "response"),
            [([0.0], time(8, 14), "ow", False),
            ([0.0], time(8, 14), "owocowa", True),
            ([1.0], time(8, 14), "owoc owoc", True),
            ([1.0], time(8, 14), " owWoWOWOwO ", True),
            ([1.0], time(8, 14), "oW", False),
            ([2.0], time(8, 14), "oW", False),
            ([3.0], time(8, 14), "oW", False),
            ([4.0], time(8, 14), "oW", False),
            ([5.0], time(8, 14), "oW", False),
            ([6.0], time(8, 14), "oW", False),
            ([7.0], time(8, 14), "oW", False),
            ([8.0], time(8, 14), "oW", False),
            ([1.0], time(8, 14), "owocy morza", True),
            ([2.0], time(8, 14), "owocy morza", True),
            ([3.0], time(8, 14), "owocy morza", True),
            ([4.0], time(8, 14), "owocy morza", True),
            ([5.0], time(8, 14), "owocy morza", True),
            ([6.0], time(8, 14), "owocy morza", False),
            ([7.0], time(8, 14), "owocy morza", False),
            ([8.0], time(8, 14), "owocy morza", False),
            ([1.0], time(9, 14), "owocy morza", False),
            ([2.0], time(8, 15), "owocy morza", False),
            ([3.0], time(18, 14), "owocy morza", False),
            ([4.0], time(8, 14), "", True),
            ([5.0], time(8, 14), "owocy morza", True),
            ([6.0], time(8, 14), "ow", False)]
    )
    def test_check_zaprawa(self, order, list_of_courses, times, name, response):
        order.list_of_courses = list_of_courses
        order.times = times
        order.name = name
        result  = order.check_zaprawa()
        assert result == response


