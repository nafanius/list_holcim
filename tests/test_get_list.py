from faker import Faker
import pytest
from datetime import datetime
from pprint import pprint
from src.get_lista import find_day_request
from unittest.mock import patch, MagicMock
from datetime import time as datetime_time
from src.get_lista import form_lista
from src.get_lista import form_lista_beton
from src.get_lista import lista_in_text
from src.get_lista import lista_in_text_beton
from src.get_lista import combination_of_some_days_list


@pytest.mark.parametrize(
    "mock_date, expected_date",
    [(datetime(2023, 3, 6), [(0,
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

class TestFormLista:
    @pytest.fixture
    def mock_openpyxl(self):
        with patch("src.get_lista.openpyxl") as mock_openpyxl:
            yield mock_openpyxl

    @pytest.fixture(scope='class')
    def mock_db_and_settings(self):
        with patch("src.get_lista.data_sql") as mock_data_sql, \
                patch("src.get_lista.Settings") as mock_settings, \
                patch("src.get_lista.db_lock"), \
                patch("src.get_lista.time") as mock_time:
            mock_settings.time_of_compare = 1
            mock_time.time.return_value = 10000
            yield mock_data_sql, mock_settings, mock_time

    @pytest.fixture(scope='class')
    def wenzel(self):
        # wenzel[1][0] and wenzel[1][1] are used for matching
        return ("zawod", ("zawodzie 2 ", "zawodzie 1 "), 24)

    def make_mock_sheet(self, rows):
        mock_sheet = MagicMock()
        mock_sheet.max_row = len(rows) + 1

        def cell(row, column):
            # row and column are 1-based
            try:
                value = rows[row-1][column-1]
            except IndexError:
                value = None
            mock_cell = MagicMock()
            mock_cell.value = value
            return mock_cell
        mock_sheet.cell.side_effect = cell
        return mock_sheet

    def test_form_lista_returns_empty_on_file_error(self, mock_openpyxl, mock_db_and_settings, wenzel):
        # Simulate file not found
        mock_openpyxl.load_workbook.side_effect = Exception("File not found")
        with patch("src.get_lista.inf") as mock_inf:
            result = form_lista("nofile.xlsx", 0, "01.01.2024", wenzel)
            assert result == []
            mock_inf.assert_any_call(
                "Such file does not exist" + "nofile.xlsx")

    @pytest.mark.parametrize(("rows", "expected"),
                             [([
                                 [None, None, "zawodzie 2 zxsxcd cdcd ", None, None,
                                     None, None, None, None, None, None, None, None],
                                 [None, None, None, None, None, None, None, None, None,
                                     None, "Driver1", "08:00", None, "Driver2", "09:30"],
                                 [None, None, None, None, None, None, None, None, None,
                                     None, "Driver3", "10:15", None, "Driver4", "11:45"],
                                 [None, None, None, None, None, None, None, None, None,
                                     None, "Driver7", "11:50", None, "Driver8", "12:45"],
                                 [None, None, None, None, None, None, None, None, None,
                                     None, "Driver9", "13:15", None, "Driver10", "13:45"],
                             ], [
                                 (datetime_time(8, 0), "Driver1"),
                                 (datetime_time(9, 30), "Driver2"),
                                 (datetime_time(10, 15), "Driver3"),
                                 (datetime_time(11, 45), "Driver4"),
                                 (datetime_time(11, 50), "Driver7"),
                                 (datetime_time(12, 45), "Driver8"),
                                 (datetime_time(13, 15), "Driver9"),
                                 (datetime_time(13, 45), "Driver10"),
                             ]),  # check if the first row is not included zawodzie 2
        ([
            [None, None, "zawodzie 1 zxsxcd cdcd ", None, None,
             None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver1", "08:00", None, "Driver2", "09:30"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver3", "10:15", None, "Driver4", "11:45"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver7", "11:50", None, "Driver8", "12:45"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver9", "13:15", None, "Driver10", "13:45"],
        ], [
            (datetime_time(8, 0), "Driver1"),
            (datetime_time(9, 30), "Driver2"),
            (datetime_time(10, 15), "Driver3"),
            (datetime_time(11, 45), "Driver4"),
            (datetime_time(11, 50), "Driver7"),
            (datetime_time(12, 45), "Driver8"),
            (datetime_time(13, 15), "Driver9"),
            (datetime_time(13, 45), "Driver10"),
        ]),  # check if the first row is not included zawodzie 1
        ([
            [None, None, "zawodzie  zxsxcd cdcd ", None, None,
             None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver1", "08:00", None, "Driver2", "09:30"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver3", "10:15", None, "Driver4", "11:45"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver7", "11:50", None, "Driver8", "12:45"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver9", "13:15", None, "Driver10", "13:45"],
        ], []),  # check if the first row is not included zawodzie 1 or zawodzie 2
        ([
            [None, None, "zawodzie 1 zxsxcd cdcd ", None, None,
             None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver1", "08,00", None, "Driver2", "09:30"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver3", "10", None, "Driver4", "11:45"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver7", "11:50", None, "Driver8", "25:45"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver9", None, None, "Driver10", "13:45"],
        ], [
            (datetime_time(9, 30), "Driver2"),
            (datetime_time(11, 45), "Driver4"),
            (datetime_time(11, 50), "Driver7"),
            (datetime_time(13, 45), "Driver10"),
        ]),  # check if the first row is not included zawodzie 1 or zawodzie 2 and the time is correct
        ([
            [None, None, "zawodzie 1 zxsxcd cdcd ", None, None,
             None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver1", "08,00", None, "Driver2", "09:30"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver3", "10", None, "Driver4", "11:45"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver7", "11:50", None, "Driver8", "25:45"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver9", None, None, "Driver10", "13:45"],
            [None, None, "zawodzi zxsxcd cdcd ", None, None,
             None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver1", "08,00", None, "Driver2", "09:30"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver3", "10", None, "Driver4", "11:45"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver7", "11:50", None, "Driver8", "25:45"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver9", None, None, "Driver10", "13:45"],
        ], [
            (datetime_time(9, 30), "Driver2"),
            (datetime_time(11, 45), "Driver4"),
            (datetime_time(11, 50), "Driver7"),
            (datetime_time(13, 45), "Driver10"),
        ]),  # check if the first row is not included zawodzie 1 or zawodzie 2 and two part of the rows not included zawodzie 1 or zawodzie 2

    ])
    def test_form_lista_returns_correct_list(self, mock_openpyxl, mock_db_and_settings, wenzel, rows, expected):
        # Prepare a fake sheet with two matching rows and valid times
        # Row 1: column 3 matches wenzel[1][0], columns 11 and 14 have names, columns 12 and 15 have times

        mock_sheet = self.make_mock_sheet(rows)
        mock_wb = MagicMock()
        mock_wb.sheetnames = ["Sheet1"]
        mock_wb.__getitem__.return_value = mock_sheet
        mock_openpyxl.load_workbook.return_value = mock_wb

        result = form_lista("file.xlsx", 0, "01.01.2024", wenzel)
        assert result == expected

    @pytest.mark.parametrize(("rows", "expected"),
                             [([
                                 [None, None, "zawodzie 2 zxsxcd cdcd ", None, None,
                                     None, None, None, None, None, None, None, None],
                                 [None, None, None, None, None, None, None, None, None,
                                     None, "Driver1", "08:00", None, "Driver2", "09:30"],
                                 [None, None, None, None, None, None, None, None, None,
                                     None, "Driver3", "10:15", None, "Driver4", "11:45"],
                                 [None, None, None, None, None, None, None, None, None,
                                     None, "Driver7", "11:50", None, "Driver3", "12:45"],
                                 [None, None, None, None, None, None, None, None, None,
                                     None, "Driver9", "13:15", None, "Driver1", "13:45"],
                             ], [
                                 (datetime_time(8, 0), "Driver1"),
                                 (datetime_time(9, 30), "Driver2"),
                                 (datetime_time(10, 15), "Driver3"),
                                 (datetime_time(11, 45), "Driver4"),
                                 (datetime_time(11, 50), "Driver7"),
                                 (datetime_time(13, 15), "Driver9"),
                             ]),
        ([
            [None, None, "zawodzie 1 zxsxcd cdcd ", None, None,
             None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver1", "08:00", None, "Driver1", "09:30"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver3", "10:15", None, "Driver4", "10:15"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver8", "11:50", None, "Driver8", "12:45"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver9", "13:15", None, "Driver10", "13:45"],
            [None, None, "zawodzie 2 zxsxcd cdcd ", None, None,
             None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver1", "08:00", None, "Driver1", "09:30"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver3", "10:15", None, "Driver4", "10:15"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver8", "11:50", None, "Driver8", "12:45"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver9", "13:15", None, "Driver10", "13:45"],
        ], [
            (datetime_time(8, 0), "Driver1"),
            (datetime_time(10, 15), "Driver3"),
            (datetime_time(10, 15), "Driver4"),
            (datetime_time(11, 50), "Driver8"),
            (datetime_time(13, 15), "Driver9"),
            (datetime_time(13, 45), "Driver10"),
        ]),
        ([
            [None, None, "zawodzie 1 zxsxcd cdcd ", None, None,
             None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver1", "08,00", None, "Driver2", "09:30"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver3", "10", None, "Driver4", "11:45"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver7", "11:50", None, "Driver8", "25:45"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver9", None, None, "Driver10", "13:45"],
            [None, None, "zawodzie 2 zxsxcd ", None, None,
             None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver1", "08,00", None, "Driver2", "09:30"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver3", "11:47", None, "Driver4", "11:45"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver17", "11:50", None, "Driver8", "25:45"],
            [None, None, None, None, None, None, None, None, None,
             None, "Driver9", None, None, "Driver11", "13:40"],
        ], [
            (datetime_time(9, 30), "Driver2"),
            (datetime_time(11, 45), "Driver4"),
            (datetime_time(11, 47), "Driver3"),
            (datetime_time(11, 50), "Driver7"),
            (datetime_time(11, 50), "Driver17"),
            (datetime_time(13, 40), "Driver11"),
            (datetime_time(13, 45), "Driver10"),
        ]),
    ])
    def test_form_lista_removes_duplicates_and_sorts(self, mock_openpyxl, mock_db_and_settings, wenzel, rows, expected):
        # Same name appears twice, only first occurrence should be kept

        mock_sheet = self.make_mock_sheet(rows)
        mock_wb = MagicMock()
        mock_wb.sheetnames = ["Sheet1"]
        mock_wb.__getitem__.return_value = mock_sheet
        mock_openpyxl.load_workbook.return_value = mock_wb

        result = form_lista("file.xlsx", 0, "01.01.2024", wenzel)
        # Only the first occurrence of "Driver" should be kept, with the earliest time
        assert result == expected

    def test_form_lista_handles_no_matches(self, mock_openpyxl, mock_db_and_settings, wenzel):
        # No row matches wenzel[1][0] or wenzel[1][1]
        rows = [
            [None, None, "zzz", None, None, None, None, None, None,
                None, "DriverX", "12:00", None, "DriverY", "13:00"],
        ]
        mock_sheet = self.make_mock_sheet(rows)
        mock_wb = MagicMock()
        mock_wb.sheetnames = ["Sheet1"]
        mock_wb.__getitem__.return_value = mock_sheet
        mock_openpyxl.load_workbook.return_value = mock_wb

        result = form_lista("file.xlsx", 0, "01.01.2024", wenzel)
        assert result == []

    def test_form_lista_ignores_invalid_times(self, mock_openpyxl, mock_db_and_settings, wenzel):
        # Invalid time strings should be ignored
        rows = [
            [None, None, "abc", None, None, None, None, None, None,
                None, "Driver1", "notatime", None, "Driver2", "25:99"],
        ]
        mock_sheet = self.make_mock_sheet(rows)
        mock_wb = MagicMock()
        mock_wb.sheetnames = ["Sheet1"]
        mock_wb.__getitem__.return_value = mock_sheet
        mock_openpyxl.load_workbook.return_value = mock_wb

        result = form_lista("file.xlsx", 0, "01.01.2024", wenzel)
        assert result == []

class TestFormListaBeton:

    @pytest.fixture
    def mock_openpyxl(self):
        with patch("src.get_lista.openpyxl") as mock_openpyxl:
            yield mock_openpyxl

    @pytest.fixture
    def mock_settings(self, monkeypatch):
        # Patch inf, lg, timer, and db/data_sql dependencies
        monkeypatch.setattr("src.get_lista.inf", lambda *a, **k: None)
        monkeypatch.setattr("src.get_lista.lg", lambda *a, **k: None)
        monkeypatch.setattr("src.get_lista.timer", lambda f: f)
        monkeypatch.setattr("src.get_lista.data_sql", MagicMock())
        monkeypatch.setattr("src.get_lista.db_lock", MagicMock())
        monkeypatch.setattr("src.get_lista.get_del_new_lists", MagicMock())
        yield

    @pytest.fixture
    def wenzel(self):
        # wenzel[1][0] and wenzel[1][1] are used for matching
        return ("zawod", ("zawodzie 2 ", "zawodzie 1 "), 24)

    def make_mock_sheet(self, rows, cols, data):
        """Helper to create a mock sheet with .cell(row, column).value"""
        sheet = MagicMock()

        def cell(row, column):
            val = data.get((row, column), None)
            m = MagicMock()
            m.value = val
            return m
        sheet.cell.side_effect = cell
        sheet.max_row = rows
        return sheet

    def test_form_lista_beton_file_not_found(self, mock_openpyxl, mock_settings, wenzel):
        # Simulate file not found
        mock_openpyxl.load_workbook.side_effect = Exception("File not found")
        result = form_lista_beton("nofile.xlsx", 0, "12.03.2024", wenzel)
        assert result == []

    def test_form_lista_beton_empty_sheet(self, mock_openpyxl, mock_settings, wenzel):
        # Sheet with no matching rows
        mock_wb = MagicMock()
        mock_sheet = self.make_mock_sheet(5, 5, {})
        mock_wb.sheetnames = ["Sheet1"]
        mock_wb.__getitem__.return_value = mock_sheet
        mock_openpyxl.load_workbook.return_value = mock_wb

        # Patch check_del_add_lista to return empty lists
        with patch("src.get_lista.get_del_new_lists.check_del_add_lista", return_value=([], [])):
            result = form_lista_beton("file.xlsx", 0, "12.03.2024", wenzel)
            assert isinstance(result, tuple)
            assert result[0] == []
            assert result[1] == []
            assert result[2] == []

    @pytest.mark.parametrize(("data_param", "count", "wenz"),
                             [({
                                 (1, 3): "zawodzie 2 ",
                                 (12, 3): Faker().time(pattern="%H:%M", end_datetime=None),
                                 (12, 7): 10.5,
                                 (12, 4): Faker().company(),
                                 (12, 5): Faker().address(),
                                 (12, 13): Faker().text(max_nb_chars=100)[:50],
                                 (12, 15): Faker().text(max_nb_chars=100)[:50],
                                 (12, 16): Faker().text(max_nb_chars=100)[:50],
                                 (12, 17): Faker().text(max_nb_chars=100)[:50],
                                 (12, 14): Faker().phone_number(),
                                 (12, 11): Faker().text(max_nb_chars=100)[:50],
                             }, 1, "2"),
        ({
            (1, 3): "zawodzie 1 ",
            (12, 3): Faker().time(pattern="%H:%M", end_datetime=None),
            (12, 7): 10.5,
            (12, 4): Faker().company(),
            (12, 5): Faker().address(),
            (12, 13): Faker().text(max_nb_chars=100)[:50],
            (12, 15): Faker().text(max_nb_chars=100)[:50],
            (12, 16): Faker().text(max_nb_chars=100)[:50],
            (12, 17): Faker().text(max_nb_chars=100)[:50],
            (12, 14): Faker().msisdn(),
            (12, 11): Faker().text(max_nb_chars=100)[:50],
            (13, 3): Faker().time(pattern="%H:%M", end_datetime=None),
            (13, 7): 10.5,
            (13, 4): Faker().company(),
            (13, 5): Faker().address(),
            (13, 13): Faker().text(max_nb_chars=100)[:50],
            (13, 15): Faker().text(max_nb_chars=100)[:50],
            (13, 16): Faker().text(max_nb_chars=100)[:50],
            (13, 17): Faker().text(max_nb_chars=100)[:50],
            (13, 14): Faker().msisdn(),
            (13, 11): Faker().text(max_nb_chars=100)[:50],
        }, 2, "1"),
        ({
            (1, 3): "zawodzi",
            (12, 3): Faker().time(pattern="%H:%M", end_datetime=None),
            (12, 7): 10.5,
            (12, 4): Faker().company(),
            (12, 5): Faker().address(),
            (12, 13): Faker().text(max_nb_chars=100)[:50],
            (12, 15): Faker().text(max_nb_chars=100)[:50],
            (12, 16): Faker().text(max_nb_chars=100)[:50],
            (12, 17): Faker().text(max_nb_chars=100)[:50],
            (12, 14): Faker().msisdn(),
            (12, 11): Faker().text(max_nb_chars=100)[:50],
            (13, 3): Faker().time(pattern="%H:%M", end_datetime=None),
            (13, 7): 10.5,
            (13, 4): Faker().company(),
            (13, 5): Faker().address(),
            (13, 13): Faker().text(max_nb_chars=100)[:50],
            (13, 15): Faker().text(max_nb_chars=100)[:50],
            (13, 16): Faker().text(max_nb_chars=100)[:50],
            (13, 17): Faker().text(max_nb_chars=100)[:50],
            (13, 14): Faker().msisdn(),
            (13, 11): Faker().text(max_nb_chars=100)[:50],
        }, 0, None),
        ({
            (1, 3): "zawodzie 1 ",
            (12, 3): Faker().time(pattern="%H:%M", end_datetime=None),
            (12, 7): 10.5,
            (12, 4): Faker().company(),
            (12, 5): Faker().address(),
            (12, 13): Faker().text(max_nb_chars=100)[:50],
            (12, 15): Faker().text(max_nb_chars=100)[:50],
            (12, 16): Faker().text(max_nb_chars=100)[:50],
            (12, 17): Faker().text(max_nb_chars=100)[:50],
            (12, 14): Faker().msisdn(),
            (12, 11): Faker().text(max_nb_chars=100)[:50],
            (15, 3): Faker().time(pattern="%H:%M", end_datetime=None),
            (15, 7): 10.5,
            (15, 4): Faker().company(),
            (15, 5): Faker().address(),
            (15, 13): Faker().text(max_nb_chars=100)[:50],
            (15, 15): Faker().text(max_nb_chars=100)[:50],
            (15, 16): Faker().text(max_nb_chars=100)[:50],
            (15, 17): Faker().text(max_nb_chars=100)[:50],
            (15, 14): Faker().msisdn(),
            (15, 11): Faker().text(max_nb_chars=100)[:50],
        }, 2, "1"),
        ({
            (1, 3): "zawodzie 1 ",
            (12, 3): "12",
            (12, 7): 10.5,
            (12, 4): Faker().company(),
            (12, 5): Faker().address(),
            (12, 13): Faker().text(max_nb_chars=100)[:50],
            (12, 15): Faker().text(max_nb_chars=100)[:50],
            (12, 16): Faker().text(max_nb_chars=100)[:50],
            (12, 17): Faker().text(max_nb_chars=100)[:50],
            (12, 14): Faker().msisdn(),
            (12, 11): Faker().text(max_nb_chars=100)[:50],
            (15, 3): Faker().time(pattern="%H:%M", end_datetime=None),
            (15, 7): 10.5,
            (15, 4): Faker().company(),
            (15, 5): Faker().address(),
            (15, 13): Faker().text(max_nb_chars=100)[:50],
            (15, 15): Faker().text(max_nb_chars=100)[:50],
            (15, 16): Faker().text(max_nb_chars=100)[:50],
            (15, 17): Faker().text(max_nb_chars=100)[:50],
            (15, 14): Faker().msisdn(),
            (15, 11): Faker().text(max_nb_chars=100)[:50],
        }, 1, "1"),
    ]
    )
    def test_form_lista_beton_with_data(self, mock_openpyxl, mock_settings, wenzel, data_param, count, wenz):
        mock_wb = MagicMock()
        mock_sheet = self.make_mock_sheet(50, 20, data_param)
        mock_wb.sheetnames = ["Sheet1"]
        mock_wb.__getitem__.return_value = mock_sheet
        mock_openpyxl.load_workbook.return_value = mock_wb

        with patch("src.get_lista.get_del_new_lists.check_del_add_lista", return_value=(["del"], ["add"])):
            result = form_lista_beton("file.xlsx", 0, "12.03.2024", wenzel)
            lista_beton, del_lista, add_lista = result
            assert isinstance(lista_beton, list)
            assert isinstance(del_lista, list)
            assert isinstance(add_lista, list)
            assert del_lista == ["del"]
            assert add_lista == ["add"]

            pprint(lista_beton)
            assert len(list((hasattr(x[1], "hour")
                       for x in lista_beton))) == count
            assert all(hasattr(x[1], "hour") for x in lista_beton)
            assert all((x[-2] == wenz) for x in lista_beton)

class TestListaInText:
    def test_empty_list(self):
        assert lista_in_text([]) == []

    def test_single_entry(self):
        lista = [(datetime_time(8, 30), "Jan Kowalski")]
        expected = ["08:30 Jan Kowalski"]
        assert lista_in_text(lista) == expected

    @pytest.mark.parametrize(("lista", "expected"),
                             [([
                                 (datetime_time(7, 0), "Anna Nowak"),
                                 (datetime_time(12, 15), "Piotr Zielinski"),
                                 (datetime_time(16, 45), "Maria Wisniewska"),
                             ],
                                 [
                                 "07:00 Anna Nowak",
                                 "12:15 Piotr Zielinski",
                                 "16:45 Maria Wisniewska",
                             ])]

                             )
    def test_multiple_entries(self, lista, expected):

        assert lista_in_text(lista) == expected

    def test_time_with_single_digit_hour_and_minute(self):
        lista = [(datetime_time(5, 5), "Adam Malysz")]
        expected = ["05:05 Adam Malysz"]
        assert lista_in_text(lista) == expected

class TestListaInTextBeton:
    def test_empty(self):
        assert lista_in_text_beton([]) == ""

    def test_normal_entry(self):
        lista_beton = [
            (10.5, datetime_time(8, 30), "FirmaA", "Adres1", "uwagi1", "przebieg1", "123456789", "2", None, 0)
        ]
        result, metres = lista_in_text_beton(lista_beton)
        assert "08:30:00 10.5 węzeł 2" in result[0]
        assert "FirmaA" in result[1]
        assert "Adres1 uwagi1 przebieg1" in result[2]
        assert "123456789" in result[3]
        assert "dzwig" in result[4]
        assert "--------------------" in result[5]
        assert "zaplanowano metrów - 10.5" in metres

    def test_pompa_entry(self):
        lista_beton = [
            (5, datetime_time(9, 0), "FirmaB", "Adres2", "uwagi2", "przebieg2", "987654321", "1", "pompa", 0)
        ]
        result, metres = lista_in_text_beton(lista_beton)
        assert "09:00:00 5 węzeł 1" in result[0]
        assert "pompa" in result[4]
        assert "zaplanowano metrów - 5.0" in metres

    def test_delete_entry(self):
        lista_beton = [
            (7, datetime_time(10, 15), "FirmaC", "Adres3", "uwagi3", "przebieg3", "555555555", "3", None, 1)
        ]
        result, metres = lista_in_text_beton(lista_beton)
        assert all('line-through' in line for line in result)
        assert "zaplanowano metrów - 0" in metres  # delete entries do not sum

    def test_add_entry(self):
        lista_beton = [
            (12, datetime_time(11, 45), "FirmaD", "Adres4", "uwagi4", "przebieg4", "444444444", "4", None, 2)
        ]
        result, metres = lista_in_text_beton(lista_beton)
        assert all('rgb(0, 139, 7)' in line for line in result)
        assert "zaplanowano metrów - 12.0" in metres

    def test_mixed_entries(self):
        lista_beton = [
            (10, datetime_time(8, 0), "FirmaA", "Adres1", "uwagi1", "przebieg1", "1111112", "1", None, 0),
            (5, datetime_time(9, 0), "FirmaB", "Adres2", "uwagi2", "przebieg2", "222222", "2", "pompa", 2),
            (3, datetime_time(10, 0), "FirmaC", "Adres3", "uwagi3", "przebieg3", "3332332", "3", None, 1),
        ]
        result, metres = lista_in_text_beton(lista_beton)
        # Check normal
        assert "08:00:00 10 węzeł 1" in result[0]
        # Check add (green)
        assert any('rgb(0, 139, 7)' in line for line in result)
        # Check delete (red, line-through)
        assert any('line-through' in line for line in result)
        # Check sum (only normal and add)
        assert "zaplanowano metrów - 15.0" in metres

    def test_non_numeric_metres(self):
        lista_beton = [
            ("not_a_number", datetime_time(12, 0), "FirmaE", "Adres5", "uwagi5", "przebieg5", "555", "pompa 258", None, 0)
        ]
        result, metres = lista_in_text_beton(lista_beton)
        assert "not_a_number" in result[0]
        assert "zaplanowano metrów - 0" in metres

# todo make this test more useful 
class TestCombinationOfSomeDaysList:
    @pytest.fixture
    def wenzel(self):
        return ("WenzelA", ("num1", "num2"), 3)

    @pytest.fixture
    def fake_list_of_day(self):
        return [
            (0, "./excel_files/Tydz 10.2024.xlsx", "01.04.2024"),
            (1, "./excel_files/Tydz 10.2024.xlsx", "02.04.2024"),
            (2, "./excel_files/Tydz 10.2024.xlsx", "03.04.2024"),
        ]

    @pytest.fixture
    def fake_form_lista(self):
        return [
            (datetime_time(7, 0), "Jan Kowalski"),
            (datetime_time(8, 0), "Anna Nowak"),
        ]

    @pytest.fixture
    def fake_lista_in_text(self):
        return ["07:00 Jan Kowalski", "08:00 Anna Nowak"]

    @pytest.fixture
    def fake_form_lista_beton(self):
        return (
            [
                (5.0, "07:00", "FirmaA", "Budowa1", "uwagi", "przebieg", "123456789", "1", "pompa"),
            ],
            [],
            [],
        )

    @pytest.fixture
    def fake_get_list_from_three_norm_del_add(self):
        return [
            (5.0, datetime_time(7, 0), "FirmaA", "Budowa1", "uwagi", "przebieg", "123456789", "1", "pompa", 0),
        ]

    @pytest.fixture
    def fake_lista_in_text_beton(self):
        return (
            [
                "07:00:00 5.0 węzeł 1",
                "FirmaA",
                "Budowa1 uwagi przebieg",
                "123456789",
                "pompa",
                "--------------------",
            ],
            '<p style="font-weight: bold; margin-bottom: 3px">zaplanowano metrów - 5.0</p>',
        )

    @pytest.fixture
    def patch_get_lista(self):
        with patch("src.get_lista.find_day_request") as mock_find_day_request, \
             patch("src.get_lista.form_lista") as mock_form_lista, \
             patch("src.get_lista.lista_in_text") as mock_lista_in_text, \
             patch("src.get_lista.form_lista_beton") as mock_form_lista_beton, \
             patch("src.get_lista.get_list_from_three_norm_del_add") as mock_get_list_from_three_norm_del_add, \
             patch("src.get_lista.lista_in_text_beton") as mock_lista_in_text_beton:
            yield {
                "mock_find_day_request": mock_find_day_request,
                "mock_form_lista": mock_form_lista,
                "mock_lista_in_text": mock_lista_in_text,
                "mock_form_lista_beton": mock_form_lista_beton,
                "mock_get_list_from_three_norm_del_add": mock_get_list_from_three_norm_del_add,
                "mock_lista_in_text_beton": mock_lista_in_text_beton,
            }

    def test_combination_of_some_days_list_success(
        self,
        patch_get_lista,
        wenzel,
        fake_list_of_day,
        fake_form_lista,
        fake_lista_in_text,
        fake_form_lista_beton,
        fake_get_list_from_three_norm_del_add,
        fake_lista_in_text_beton,
    ):
        patch_get_lista["mock_find_day_request"].return_value = fake_list_of_day
        patch_get_lista["mock_form_lista"].return_value = fake_form_lista
        patch_get_lista["mock_lista_in_text"].return_value = fake_lista_in_text
        patch_get_lista["mock_form_lista_beton"].return_value = fake_form_lista_beton
        patch_get_lista["mock_get_list_from_three_norm_del_add"].return_value = fake_get_list_from_three_norm_del_add
        patch_get_lista["mock_lista_in_text_beton"].return_value = fake_lista_in_text_beton

        result = combination_of_some_days_list(wenzel)

        assert isinstance(result, dict)
        assert len(result) == 6
        for i in range(1, 7):
            assert f"element{i}" in result
        assert "01.04.2024 poniedziałek" in result["element1"][0]
        assert "zaplanowano metrów" in "".join(result["element4"])

    def test_combination_of_some_days_list_no_data(
        self,
        patch_get_lista,
        wenzel,
        fake_list_of_day,
    ):
        patch_get_lista["mock_find_day_request"].return_value = fake_list_of_day
        patch_get_lista["mock_form_lista"].return_value = []
        patch_get_lista["mock_lista_in_text"].return_value = []
        patch_get_lista["mock_form_lista_beton"].return_value = ([], [], [])
        patch_get_lista["mock_get_list_from_three_norm_del_add"].return_value = []
        patch_get_lista["mock_lista_in_text_beton"].side_effect = ValueError("No data")

        result = combination_of_some_days_list(wenzel)

        assert isinstance(result, dict)
        assert len(result) == 6
        for v in result.values():
            assert any("Dane są niedostępne" in str(x) for x in v)