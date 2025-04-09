from datetime import time
from statistic.driver import Driver


def test_count_driver():
    d1 = Driver("10.04.2025", time(hour=10, minute=10), "wojtek")
    d2 = Driver("10.04.2025", time(hour=10, minute=20), "wojtek1")
    d3 = Driver("10.04.2025", time(hour=10, minute=30), "wojtek2")
    d4 = Driver("10.04.2025", time(hour=10, minute=40), "wojtek3")

    assert d4.count_driver == 4


def test_field_access():
    d1 = Driver("10.04.2025", time(hour=10, minute=10), "wojtek")

    assert d1.date_order == "10.04.2025"
    assert d1.time_in_list == time(hour=10, minute=10)
    assert d1.person == "wojtek"


def test_convert_to_dict_for_df():
    d1 = Driver("10.04.2025", time(hour=10, minute=10), "wojtek")

    assert d1.convert_to_dict_for_df() == {"date_order": "10.04.2025",
                                         "time_in_list": time(hour=10, minute=10),
                                         "person": "wojtek"
                                         }


