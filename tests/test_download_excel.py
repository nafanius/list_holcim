import pytest
from datetime import datetime
from src.download_excel import generate_name_of_file_google


@pytest.mark.parametrize(
    "mock_now, expected",
    [
        # Case: First week of the year, previous year is different
        (datetime(year=2025, month=1, day=1), ["1.2025", "2.2025"]),
        # Case: Middle of the year
        (datetime(year=2025, month=6, day=15), ["24.2025", "25.2025"]),
        # Case: End of the, year end day last year in 1 week 
        (datetime(year=2025, month=12, day=31), ["1.2026", "2.2026"]),
        # Case: End of the year
        (datetime(year=2025, month=12, day=30), ["1.2026", "2.2026"]),
        # Case: End of the year
        (datetime(year=2025, month=12, day=29), ["1.2026", "2.2026"]),
        # Case: End of the year
        (datetime(year=2025, month=12, day=28), ["52.2025", "1.2026"]),
        # Case: End of the year
        (datetime(year=2024, month=12, day=29), ["52.2024", "1.2025"]),
        # Case: End of the year
        (datetime(year=2024, month=12, day=30), ["1.2025", "2.2025"]),
        # Case: End of the year
        (datetime(year=2024, month=12, day=23), ["52.2024", "1.2025"]),
        # Case: End of the year
        (datetime(year=2024, month=12, day=22), ["51.2024", "52.2024"]),
        # Case: First week of the year, same year
        (datetime(year=2026, month=1, day=2), ["1.2026", "2.2026"]),
    ],
)
def test_generate_name_of_file_google(monkeypatch, mock_now, expected):
    # Mock datetime.now() to return the mock_now value
    class MockDateTime(datetime):
        @classmethod
        def now(cls):
            return mock_now

    monkeypatch.setattr("src.download_excel.datetime", MockDateTime)

    # Call the function and assert the result
    result = generate_name_of_file_google()
    assert result == expected


