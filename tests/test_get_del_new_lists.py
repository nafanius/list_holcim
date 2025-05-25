import pytest
import time
from unittest.mock import patch, MagicMock
from src.get_del_new_lists import get_old_list_beton
from src.get_del_new_lists import check_del_add_lista


@pytest.fixture
def mock_settings(monkeypatch):
    class MockSettings:
        time_of_compare = 4
    monkeypatch.setattr("src.get_del_new_lists.Settings", MockSettings)
    return MockSettings

@pytest.fixture
def mock_data_sql(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("src.get_del_new_lists.data_sql", mock)
    return mock

class TestGetOldListBeton:
 

    def test_get_old_list_beton_calls_delete_and_get(self, monkeypatch, mock_settings, mock_data_sql):
        date_of_lista_text = "12.03.2024"
        wenzel = ("zawod",("zawodzie 2 ", "zawodzie 1 "), 24)
        hours = 4 

        # Patch time.time to return a fixed value
        fake_now = 1_000_000
        monkeypatch.setattr(time, "time", lambda: fake_now)

        # Setup mock return value
        mock_data_sql.get_oldest_list_beton_or_lista.return_value = ["record1", "record2"]

        result = get_old_list_beton(date_of_lista_text, wenzel, hours)

        expected_threshold = fake_now - hours * 3600
        mock_data_sql.delete_records_below_threshold.assert_called_once_with(expected_threshold, "beton", wenzel[0])
        mock_data_sql.get_oldest_list_beton_or_lista.assert_called_once_with("beton", date_of_lista_text, wenzel[0])
        assert result == ["record1", "record2"]

    def test_get_old_list_beton_default_hours(self, monkeypatch, mock_settings, mock_data_sql):
        date_of_lista_text = "13.03.2024"
        wenzel = ("zawod",("zawodzie 2 ", "zawodzie 1 "), 24)

        fake_now = 2_000_000
        monkeypatch.setattr(time, "time", lambda: fake_now)
        mock_data_sql.get_oldest_list_beton_or_lista.return_value = []

        result = get_old_list_beton(date_of_lista_text, wenzel)
        expected_threshold = fake_now - mock_settings.time_of_compare * 3600
        mock_data_sql.delete_records_below_threshold.assert_called_once_with(expected_threshold, "beton", wenzel[0])
        mock_data_sql.get_oldest_list_beton_or_lista.assert_called_once_with("beton", date_of_lista_text, wenzel[0])
        assert result == []

    def test_get_old_list_beton_returns_empty_if_no_records(self, monkeypatch, mock_settings, mock_data_sql):
        date_of_lista_text = "14.03.2024"
        wenzel = "W3"
        monkeypatch.setattr(time, "time", lambda: 1234567)
        mock_data_sql.get_oldest_list_beton_or_lista.return_value = []

        result = get_old_list_beton(date_of_lista_text, wenzel, 1)
        assert result == []

class TestCheckDelAddLista:
    def test_no_changes(self, monkeypatch):
        date_of_lista_text = "15.03.2024"
        wenzel = ("zawod",("zawodzie 2 ", "zawodzie 1 "), 24)
        old_list = ["a", "b", "c"]
        currant_list = ["a", "b", "c"]

        monkeypatch.setattr("src.get_del_new_lists.get_old_list_beton", lambda date_of_lista_text, wenzel: old_list)
        del_lista, add_lista = check_del_add_lista(date_of_lista_text, currant_list, wenzel)
        assert del_lista == []
        assert add_lista == []

    def test_all_removed(self, monkeypatch):
        date_of_lista_text = "16.03.2024"
        wenzel = ("zawod",("zawodzie 2 ", "zawodzie 1 "), 24)
        old_list = ["a", "b", "c"]
        currant_list = []

        monkeypatch.setattr("src.get_del_new_lists.get_old_list_beton", lambda date_of_lista_text, wenzel: old_list)
        del_lista, add_lista = check_del_add_lista(date_of_lista_text, currant_list, wenzel)
        assert del_lista == ["a", "b", "c"]
        assert add_lista == []

    def test_all_added(self, monkeypatch):
        date_of_lista_text = "17.03.2024"
        wenzel = ("zawod",("zawodzie 2 ", "zawodzie 1 "), 24)
        old_list = []
        currant_list = ["x", "y"]

        monkeypatch.setattr("src.get_del_new_lists.get_old_list_beton", lambda date_of_lista_text, wenzel: old_list)
        del_lista, add_lista = check_del_add_lista(date_of_lista_text, currant_list, wenzel)
        assert del_lista == []
        assert add_lista == ["x", "y"]

    def test_some_added_and_removed(self, monkeypatch):
        date_of_lista_text = "18.03.2024"
        wenzel = ("zawod",("zawodzie 2 ", "zawodzie 1 "), 24)
        old_list = ["a", "b", "c"]
        currant_list = ["b", "c", "d", "e"]

        monkeypatch.setattr("src.get_del_new_lists.get_old_list_beton", lambda date_of_lista_text, wenzel: old_list)
        del_lista, add_lista = check_del_add_lista(date_of_lista_text, currant_list, wenzel)
        assert del_lista == ["a"]
        assert add_lista == ["d", "e"]

    def test_duplicates_in_lists(self, monkeypatch):
        date_of_lista_text = "19.03.2024"
        wenzel = ("zawod",("zawodzie 2 ", "zawodzie 1 "), 24)
        old_list = ["a", "b", "b", "c"]
        currant_list = ["b", "c", "c", "d"]

        monkeypatch.setattr("src.get_del_new_lists.get_old_list_beton", lambda date_of_lista_text, wenzel: old_list)
        del_lista, add_lista = check_del_add_lista(date_of_lista_text, currant_list, wenzel)
        # "a" and one "b" are removed, "d" and one "c" are added
        assert del_lista == ["a", "b"]
        assert add_lista == ["c", "d"]
