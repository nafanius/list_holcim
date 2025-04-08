import sys
import os
# Определите путь до корня проекта
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from statistic.driver import Driver
from datetime import time


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