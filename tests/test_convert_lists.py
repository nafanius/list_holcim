import pytest
from datetime import datetime
from src.convert_lists import converter
from src.convert_lists import compare_lists_by_tuples
import copy
from src.convert_lists import get_list_from_three_norm_del_add

class TestConverter:
    @pytest.mark.parametrize(
        "input_list,expected",
        [
            (
                ["100", datetime(2024, 6, 1, 14, 30), "FirmX", "John   Doe ", "Note", "12345", "123456789", "wenz1", "1", 0],
                ["100", "14:30", "FirmX", "John Doe", "Note", "12345", "123456789", "wenz1", True, 0]
            ),
            (
                [None, datetime(2024, 6, 1, 8, 0), None, "", None, None, None, None, None, 1],
                ["", "08:00", "", "", "", "", "", None, False, 1]
            ),
            (
                ["  200  ", datetime(2024, 6, 1, 9, 15), "  Firm None ", "  Alice  ", "None", "  54321  ", "  987654321  ", "wenz2", "None", 2],
                ["200", "09:15", "Firm", "Alice", "", "54321", "987654321", "wenz2", False, 2]
            ),
            (
                ["300", datetime(2024, 6, 1, 10, 45), "FirmY", "Bob", "Remark", "67890", 123456789.0, "wenz3", "0", 3],
                ["300", "10:45", "FirmY", "Bob", "Remark", "67890", "123456789", "wenz3", True, 3]
            ),
            (
                ["400", datetime(2024, 6, 1, 12, 0), "FirmZ", "Eve", "Info", "11111", "555555555", "wenz4", "501", 4],
                ["400", "12:00", "FirmZ", "Eve", "Info", "11111", "555555555", "wenz4", False, 4]
            ),
            (
                ["500", datetime(2024, 6, 1, 13, 0), "FirmA", "Carl", "None", "22222", "666666666", "wenz5", "", 5],
                ["500", "13:00", "FirmA", "Carl", "", "22222", "666666666", "wenz5", False, 5]
            ),
        ]
    )
    def test_converter(self, input_list, expected):
        result = converter(input_list)
        assert result == expected


class TestCompareListsByTuples:
    @pytest.mark.parametrize(
        "del_lista, add_lista, expected_del, expected_add",
        [
            # No matches, lists unchanged
            (
                [
                    ["100", "14:30", "FirmX", "John", "Note", "12345", "123456789", "wenz1", True, 1],
                    ["200", "15:00", "FirmY", "Alice", "Note2", "54321", "987654321", "wenz2", False, 1],
                ],
                [
                    ["300", "16:00", "FirmZ", "Bob", "Note3", "67890", "555555555", "wenz3", True, 2],
                ],
                [
                    ["100", "14:30", "FirmX", "John", "Note", "12345", "123456789", "wenz1", True, 1],
                    ["200", "15:00", "FirmY", "Alice", "Note2", "54321", "987654321", "wenz2", False, 1],
                ],
                [
                    ["300", "16:00", "FirmZ", "Bob", "Note3", "67890", "555555555", "wenz3", True, 2],
                ],
            ),
            # One match, one field differs, HTML tags applied, add_lista element removed
            (
                [
                    ["100", "14:30", "FirmX", "John", "Note", "12345", "123456789", "wenz1", True, 1],
                ],
                [
                    ["100", "14:30", "FirmX", "Johnny", "Note", "12345", "123456789", "wenz1", True, 2],
                ],
                [
                    [
                        "100",
                        "14:30",
                        "FirmX",
                        '<span style="color: rgb(238, 36, 36); font-weight: bold; text-decoration: line-through;">John</span> <span style="color: rgb(0, 139, 7); font-weight: bold;">Johnny</span>',
                        "Note",
                        "12345",
                        "123456789",
                        "wenz1",
                        True,
                        0,
                    ]
                ],
                [],
            ),
            # Multiple matches, multiple fields differ
            (
                [
                    ["100", "14:30", "FirmX", "John", "Note", "12345", "123456789", "wenz1", True, 1],
                    ["200", "15:00", "FirmY", "Alice", "Note2", "54321", "987654321", "wenz2", False, 1],
                ],
                [
                    ["100", "14:30", "FirmX", "Johnny", "Note", "12345", "123456789", "wenz1", True, 2],
                    ["200", "15:00", "FirmY", "Alicia", "Note2", "54321", "987654321", "wenz2", True, 2],
                ],
                [
                    [
                        "100",
                        "14:30",
                        "FirmX",
                        '<span style="color: rgb(238, 36, 36); font-weight: bold; text-decoration: line-through;">John</span> <span style="color: rgb(0, 139, 7); font-weight: bold;">Johnny</span>',
                        "Note",
                        "12345",
                        "123456789",
                        "wenz1",
                        True,
                        0,
                    ],
                    [
                        "200",
                        "15:00",
                        "FirmY",
                        '<span style="color: rgb(238, 36, 36); font-weight: bold; text-decoration: line-through;">Alice</span> <span style="color: rgb(0, 139, 7); font-weight: bold;">Alicia</span>',
                        "Note2",
                        "54321",
                        "987654321",
                        "wenz2",
                        False,
                        0,
                    ],
                ],
                [],
            ),
            # Partial match, only one tuple matches
            (
                [
                    ["100", "14:30", "FirmX", "John", "Note", "12345", "123456789", "wenz1", True, 1],
                    ["200", "15:00", "FirmY", "Alice", "Note2", "54321", "987654321", "wenz2", False, 1],
                ],
                [
                    ["100", "14:30", "FirmX", "Johnny", "Note", "12345", "123456789", "wenz1", True, 2],
                    ["300", "16:00", "FirmZ", "Bob", "Note3", "67890", "555555555", "wenz3", True, 2],
                ],
                [
                    [
                        "100",
                        "14:30",
                        "FirmX",
                        '<span style="color: rgb(238, 36, 36); font-weight: bold; text-decoration: line-through;">John</span> <span style="color: rgb(0, 139, 7); font-weight: bold;">Johnny</span>',
                        "Note",
                        "12345",
                        "123456789",
                        "wenz1",
                        True,
                        0,
                    ],
                    ["200", "15:00", "FirmY", "Alice", "Note2", "54321", "987654321", "wenz2", False, 1],
                ],
                [
                    ["300", "16:00", "FirmZ", "Bob", "Note3", "67890", "555555555", "wenz3", True, 2],
                ],
            ),
        ]
    )
    def test_compare_lists_by_tuples(self, del_lista, add_lista, expected_del, expected_add):
        # Deepcopy to avoid mutation side effects
        del_copy = copy.deepcopy(del_lista)
        add_copy = copy.deepcopy(add_lista)
        result_del, result_add = compare_lists_by_tuples(del_copy, add_copy)
        assert result_del == expected_del
        assert result_add == expected_add


class TestGetListFromThreeNormDelAdd:
    @pytest.mark.parametrize(
        "lista_norm, lista_del, lista_add, expected",
        [
            # All lists empty
            ([], [], [], []),

            # Only norm list has items
            (
                [
                    ("100", datetime(2024, 6, 1, 14, 30), "FirmX", "John", "Note ", "12345", "  123456789", "wenz1", "1"),
                ],
                [],
                [],
                [
                    ["100", "14:30", "FirmX", "John", "Note", "12345", "123456789", "wenz1", True, 0],
                ],
            ),

            # Only del list has items
            (
                [],
                [
                    ("200", datetime(2024, 6, 1, 15, 0), "FirmY", "Alice", "Note    2", "54321", "987654321", "wenz2", None),
                ],
                [],
                [
                    ["200", "15:00", "FirmY", "Alice", "Note 2", "54321", "987654321", "wenz2", False, 1],
                ],
            ),

            # Only add list has items
            (
                [("300", datetime(2024, 6, 1, 16, 0), "FirmZ", "Bob", "Note3", "67890", "555555555", "wenz3", "hsjhdaj"),],
                [],
                [
                    ("300", datetime(2024, 6, 1, 16, 0), "FirmZ", "Bob", "Note3", "67890", "555555555", "wenz3", "hsjhdaj"),
                ],
                [
                    ["300", "16:00", "FirmZ", "Bob", "Note3", "67890", "555555555", "wenz3", True, 2],
                ],
            ),

            # All lists have unique items
            (
                [
                    ("100", datetime(2024, 6, 1, 14, 30), "FirmX", "John", "Note", "12345", "123456789", "wenz1", "saddaccas"),
                    ("200", datetime(2024, 6, 1, 15, 0), "FirmY", "Alice", "Note2", "54321", "987654321", "wenz2", "501"),
                    ("300", datetime(2024, 6, 1, 16, 0), "FirmZ", "Bob", "Note3", "67890", "555555555", "wenz3", "1"),
                ],
                [
                    ("200", datetime(2024, 6, 1, 15, 0), "FirmY", "Alice", "Note2", "54321", "987654321", "wenz2", "501"),
                ],
                [
                    ("300", datetime(2024, 6, 1, 16, 0), "FirmZ", "Bob", "Note3", "67890", "555555555", "wenz3", "1"),
                ],
                [
                    ["100", "14:30", "FirmX", "John", "Note", "12345", "123456789", "wenz1", True, 0],
                    ["200", "15:00", "FirmY", "Alice", "Note2", "54321", "987654321", "wenz2", False, 1],
                    ["300", "16:00", "FirmZ", "Bob", "Note3", "67890", "555555555", "wenz3", True, 2],
                ],
            ),

            # Overlapping: norm and add have same tuple (should prefer add version)
            (
                [
                    ("100", datetime(2024, 6, 1, 14, 30), "FirmX", "Johnny", "Note", "12345", "123456789", "wenz1", None),
                ],
                [],
                [
                    ("100", datetime(2024, 6, 1, 14, 30), "FirmX", "Johnny", "Note", "12345", "123456789", "wenz1", None),
                ],
                [
                    ["100", "14:30", "FirmX", "Johnny", "Note", "12345", "123456789", "wenz1", False, 2],
                ],
            ),

            # Overlapping: del and add have same first 3 elements, should merge with HTML and remove from add
            (
                [   
                    ("100", datetime(2024, 6, 1, 14, 30), "FirmX", "Johnny", "Note", "12345", "123456789", "wenz1", "1"),
                ],
                [
                    ("100", datetime(2024, 6, 1, 14, 30), "FirmX", "John", "Note", "12345", "", "wenz1", "1"),
                ],
                [
                    ("100", datetime(2024, 6, 1, 14, 30), "FirmX", "Johnny", "Note", "12345", "123456789", "wenz1", "1"),
                ],
                [
                    [
                        "100",
                        "14:30",
                        "FirmX",
                        '<span style="color: rgb(238, 36, 36); font-weight: bold; text-decoration: line-through;">John</span> <span style="color: rgb(0, 139, 7); font-weight: bold;">Johnny</span>',
                        "Note",
                        "12345",
                        '<span style="color: rgb(238, 36, 36); font-weight: bold; text-decoration: line-through;"></span> <span style="color: rgb(0, 139, 7); font-weight: bold;">123456789</span>',
                        "wenz1",
                        True,
                        0,
                    ]
                ],
            ),

           
        ]
    )
    def test_get_list_from_three_norm_del_add(self, lista_norm, lista_del, lista_add, expected):
        result = get_list_from_three_norm_del_add(lista_norm, lista_del, lista_add)
        assert result == expected





