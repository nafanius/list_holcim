import sys
import os
# Определите путь до корня проекта
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

import pandas as pd
from pandas.testing import assert_frame_equal
from statistic.adjust_time import adjust_time1
from statistic.adjust_time import adjust_times

def test_adjust_time1_two_orders():
    data = {
        'time': [pd.Timestamp('2023-01-01 10:00:00'), pd.Timestamp('2023-01-01 10:00:00')],
        'wenz': ['A', 'A']
    }
    df = pd.DataFrame(data)
    expected_data = {
        'time': [pd.Timestamp('2023-01-01 09:55:00'), pd.Timestamp('2023-01-01 10:00:00')],
        'wenz': ['A', 'A']
    }
    expected_df = pd.DataFrame(expected_data)
    result_df = adjust_time1(df)
    assert_frame_equal(result_df.sort_index(axis=1), expected_df.sort_index(axis=1))

def test_adjust_time1_three_orders():
    data = {
        'time': [pd.Timestamp('2023-01-01 10:00:00')] * 3,
        'wenz': ['A', 'A', 'A']
    }
    df = pd.DataFrame(data)
    expected_data = {
        'time': [pd.Timestamp('2023-01-01 09:55:00'), pd.Timestamp('2023-01-01 10:00:00'), pd.Timestamp('2023-01-01 10:05:00')],
        'wenz': ['A', 'A', 'A']
    }
    expected_df = pd.DataFrame(expected_data)
    result_df = adjust_time1(df)
    assert_frame_equal(result_df.sort_index(axis=1), expected_df.sort_index(axis=1))

def test_adjust_time1_four_orders():
    data = {
        'time': [pd.Timestamp('2023-01-01 10:00:00')] * 4,
        'wenz': ['A', 'A', 'A', 'A']
    }
    df = pd.DataFrame(data)
    expected_data = {
        'time': [
            pd.Timestamp('2023-01-01 09:50:00'),
            pd.Timestamp('2023-01-01 09:55:00'),
            pd.Timestamp('2023-01-01 10:00:00'),
            pd.Timestamp('2023-01-01 10:05:00')
        ],
        'wenz': ['A', 'A', 'A', 'A']
    }
    expected_df = pd.DataFrame(expected_data)
    result_df = adjust_time1(df)
    assert_frame_equal(result_df.sort_index(axis=1), expected_df.sort_index(axis=1))

def test_adjust_time1_five_orders():
    data = {
        'time': [pd.Timestamp('2023-01-01 10:00:00')] * 5,
        'wenz': ['A', 'A', 'A', 'A', 'A']
    }
    df = pd.DataFrame(data)
    expected_data = {
        'time': [
            pd.Timestamp('2023-01-01 09:50:00'),
            pd.Timestamp('2023-01-01 09:55:00'),
            pd.Timestamp('2023-01-01 10:00:00'),
            pd.Timestamp('2023-01-01 10:05:00'),
            pd.Timestamp('2023-01-01 10:10:00')
        ],
        'wenz': ['A', 'A', 'A', 'A', 'A']
    }
    expected_df = pd.DataFrame(expected_data)
    result_df = adjust_time1(df)
    assert_frame_equal(result_df.sort_index(axis=1), expected_df.sort_index(axis=1))

def test_adjust_time1_five_orders_multygroup():
    data = {
        'time': [pd.Timestamp('2023-01-01 10:00:00')] * 15,
        'wenz': ['A', 'A', 'A', 'B', 'B', 'A', 'A', 'A', 'B', 'B', 'A', 'B', 'B', 'A', 'A']
    }
    df = pd.DataFrame(data)
    expected_data = {
        'time': [
            pd.Timestamp('2023-01-01 09:49:00'),
            pd.Timestamp('2023-01-01 09:50:00'),
            pd.Timestamp('2023-01-01 09:50:00'),
            pd.Timestamp('2023-01-01 09:54:00'),
            pd.Timestamp('2023-01-01 09:54:00'),
            pd.Timestamp('2023-01-01 09:55:00'),
            pd.Timestamp('2023-01-01 09:55:00'),
            pd.Timestamp('2023-01-01 10:00:00'),
            pd.Timestamp('2023-01-01 10:00:00'),
            pd.Timestamp('2023-01-01 10:05:00'),
            pd.Timestamp('2023-01-01 10:05:00'),
            pd.Timestamp('2023-01-01 10:06:00'),
            pd.Timestamp('2023-01-01 10:10:00'),
            pd.Timestamp('2023-01-01 10:10:00'),
            pd.Timestamp('2023-01-01 10:11:00')
        ],
        'wenz': ['A', 'A', 'B', 'A', 'B','A', 'B', 'A', 'B', 'A','B', 'A', 'A', 'B', 'A']
    }
    expected_df = pd.DataFrame(expected_data)
    result_df = adjust_time1(df)
    result_df.reset_index(drop=True, inplace=True)

    assert_frame_equal(result_df, expected_df)

def test_adjust_time1_no_changes():
    data = {
        'time': [pd.Timestamp('2023-01-01 10:00:00'), pd.Timestamp('2023-01-01 10:10:00')],
        'wenz': ['A', 'A']
    }
    df = pd.DataFrame(data)
    expected_df = df.copy()
    result_df = adjust_time1(df)
    assert_frame_equal(result_df.sort_index(axis=1), expected_df.sort_index(axis=1))
    def test_adjust_times_combined_adjustments():
        data = {
            'time': [
                pd.Timestamp('2023-01-01 10:00:00'),
                pd.Timestamp('2023-01-01 10:00:00'),
                pd.Timestamp('2023-01-01 10:05:00'),
                pd.Timestamp('2023-01-01 10:10:00')
            ],
            'wenz': ['A', 'A', 'B', 'B']
        }
        df = pd.DataFrame(data)
        expected_data = {
            'time': [
                pd.Timestamp('2023-01-01 09:55:00'),
                pd.Timestamp('2023-01-01 10:00:00'),
                pd.Timestamp('2023-01-01 10:07:00'),
                pd.Timestamp('2023-01-01 10:14:00')
            ],
            'wenz': ['A', 'A', 'B', 'B']
        }
        expected_df = pd.DataFrame(expected_data)
        expected_df = expected_df.sort_values("time").reset_index(drop=True)
        expected_df.index = expected_df.index + 1

        result_df = adjust_times(df)
        assert_frame_equal(result_df.sort_index(axis=1), expected_df.sort_index(axis=1)) # type: ignore

    def test_adjust_times_no_changes_needed():
        data = {
            'time': [
                pd.Timestamp('2023-01-01 10:00:00'),
                pd.Timestamp('2023-01-01 10:10:00'),
                pd.Timestamp('2023-01-01 10:20:00'),
                pd.Timestamp('2023-01-01 10:30:00')
            ],
            'wenz': ['A', 'A', 'B', 'B']
        }
        df = pd.DataFrame(data)
        expected_df = df.copy()
        expected_df = expected_df.sort_values("time").reset_index(drop=True)
        expected_df.index = expected_df.index + 1

        result_df = adjust_times(df)
        assert_frame_equal(result_df.sort_index(axis=1), expected_df.sort_index(axis=1)) # type: ignore

    def test_adjust_times_multiple_groups():
        data = {
            'time': [
                pd.Timestamp('2023-01-01 10:00:00'),
                pd.Timestamp('2023-01-01 10:00:00'),
                pd.Timestamp('2023-01-01 10:00:00'),
                pd.Timestamp('2023-01-01 10:10:00'),
                pd.Timestamp('2023-01-01 10:10:00'),
                pd.Timestamp('2023-01-01 10:10:00')
            ],
            'wenz': ['A', 'A', 'A', 'B', 'B', 'B']
        }
        df = pd.DataFrame(data)
        expected_data = {
            'time': [
                pd.Timestamp('2023-01-01 09:55:00'),
                pd.Timestamp('2023-01-01 10:00:00'),
                pd.Timestamp('2023-01-01 10:05:00'),
                pd.Timestamp('2023-01-01 10:05:00'),
                pd.Timestamp('2023-01-01 10:10:00'),
                pd.Timestamp('2023-01-01 10:15:00')
            ],
            'wenz': ['A', 'A', 'A', 'B', 'B', 'B']
        }
        expected_df = pd.DataFrame(expected_data)
        expected_df = expected_df.sort_values("time").reset_index(drop=True)
        expected_df.index = expected_df.index + 1

        result_df = adjust_times(df)
        assert_frame_equal(result_df.sort_index(axis=1), expected_df.sort_index(axis=1)) # type: ignore

    def test_adjust_times_single_group():
        data = {
            'time': [
                pd.Timestamp('2023-01-01 10:00:00'),
                pd.Timestamp('2023-01-01 10:00:00'),
                pd.Timestamp('2023-01-01 10:00:00'),
                pd.Timestamp('2023-01-01 10:00:00')
            ],
            'wenz': ['A', 'A', 'A', 'A']
        }
        df = pd.DataFrame(data)
        expected_data = {
            'time': [
                pd.Timestamp('2023-01-01 09:50:00'),
                pd.Timestamp('2023-01-01 09:55:00'),
                pd.Timestamp('2023-01-01 10:00:00'),
                pd.Timestamp('2023-01-01 10:05:00')
            ],
            'wenz': ['A', 'A', 'A', 'A']
        }
        expected_df = pd.DataFrame(expected_data)
        expected_df = expected_df.sort_values("time").reset_index(drop=True)
        expected_df.index = expected_df.index + 1

        result_df = adjust_times(df)
        assert_frame_equal(result_df.sort_index(axis=1), expected_df.sort_index(axis=1)) # type: ignore
