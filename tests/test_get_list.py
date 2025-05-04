import pytest
from datetime import datetime, timedelta
from src.get_lista import find_day_request

@pytest.mark.parametrize(
    "mock_date, expected_date",
    [   (datetime(2023, 3, 6), [(0,
                                 f"./excel_files/Tydz 10.2023.xlsx",
                                 "06.03.2023"),
                                 (1,
                                 f"./excel_files/Tydz 10.2023.xlsx",
                                 "07.03.2023"),
                                 (2,
                                 f"./excel_files/Tydz 10.2023.xlsx",
                                 "08.03.2023")]),  # Monday
        (datetime(2024, 12, 23), [(0,
                                 f"./excel_files/Tydz 52.2024.xlsx",
                                 "23.12.2024"),
                                 (1,
                                 f"./excel_files/Tydz 52.2024.xlsx",
                                 "24.12.2024"),
                                 (2,
                                 f"./excel_files/Tydz 52.2024.xlsx",
                                 "25.12.2024")]),  # Tuesday
        (datetime(2024, 12, 27), [(4,
                                 f"./excel_files/Tydz 52.2024.xlsx",
                                 "27.12.2024"),
                                 (5,
                                 f"./excel_files/Tydz 52.2024.xlsx",
                                 "28.12.2024"),
                                 (0,
                                 f"./excel_files/Tydz 1.2025.xlsx",
                                 "30.12.2024")]),  # Friday
        (datetime(2024, 12, 28), [(5,
                                 f"./excel_files/Tydz 52.2024.xlsx",
                                 "28.12.2024"),
                                 (0,
                                 f"./excel_files/Tydz 1.2025.xlsx",
                                 "30.12.2024"),
                                 (1,
                                 f"./excel_files/Tydz 1.2025.xlsx",
                                 "31.12.2024")]),  # Saturday
        (datetime(2024, 12, 29), [(0,
                                 f"./excel_files/Tydz 1.2025.xlsx",
                                 "30.12.2024"),
                                 (1,
                                 f"./excel_files/Tydz 1.2025.xlsx",
                                 "31.12.2024"),
                                 (2,
                                 f"./excel_files/Tydz 1.2025.xlsx",
                                 "01.01.2025")]),  # Sunday
        (datetime(2024, 12, 30), [(0,
                                 f"./excel_files/Tydz 1.2025.xlsx",
                                 "30.12.2024"),
                                 (1,
                                 f"./excel_files/Tydz 1.2025.xlsx",
                                 "31.12.2024"),
                                 (2,
                                 f"./excel_files/Tydz 1.2025.xlsx",
                                 "01.01.2025")]),  # Monday
        (datetime(2024, 12, 31), [(1,
                                 f"./excel_files/Tydz 1.2025.xlsx",
                                 "31.12.2024"),
                                 (2,
                                 f"./excel_files/Tydz 1.2025.xlsx",
                                 "01.01.2025"),
                                 (3,
                                 f"./excel_files/Tydz 1.2025.xlsx",
                                 "02.01.2025")]),  # Tuesday
        (datetime(2025, 1, 1), [(2,
                                 f"./excel_files/Tydz 1.2025.xlsx",
                                 "01.01.2025"),
                                 (3,
                                 f"./excel_files/Tydz 1.2025.xlsx",
                                 "02.01.2025"),
                                 (4,
                                 f"./excel_files/Tydz 1.2025.xlsx",
                                 "03.01.2025")])  # Wednesday
    ]
)
def test_find_day_request(monkeypatch, mock_date, expected_date):
    class MockDateTime:
        @classmethod
        def now(cls):
            return mock_date

    # Monkeypatch datetime in the src.get_lista module
    monkeypatch.setattr("src.get_lista.datetime", MockDateTime)

    result = find_day_request()
    assert len(result) == 3
    assert result == expected_date

