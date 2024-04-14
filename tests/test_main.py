from io import StringIO

import pytest
from unittest.mock import mock_open, patch
from main import main


@pytest.fixture
def setup_main():
    yield


def test_main_successful_execution(setup_main):
    mock_file_content = "10 + 5\n7 - 3\n3 * 4\n6 / 2"

    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        main()


def test_main_exception_handling(setup_main):
    mock_file_content = "10 + 5\n7 - 3\n3 * 4\n6 / 0"

    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        main()


@pytest.mark.parametrize("input_expression, expected_result", [
    ("10 + 5", "Result: 15.0\n"),
    ("7 - 3", "Result: 4.0\n"),
    ("3 * 4", "Result: 12.0\n"),
    ("6 / 2", "Result: 3.0\n")
])
def test_main_parameterized(setup_main, input_expression, expected_result):
    mock_file_content = input_expression

    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main()

            assert expected_result in mock_stdout.getvalue()
