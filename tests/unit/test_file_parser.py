"""Unit tests for file parser."""

import pytest
from src.utils.file_parser import FileParser


def test_parse_filename():
    """Test filename parsing."""
    filename = "빅보스_부산_진구중앙_2024_11-1.xlsx"
    file_info = FileParser.parse_filename(filename)
    assert file_info.year == 2024
    assert file_info.month == 11
    assert file_info.week == 1


def test_parse_invalid_filename():
    """Test invalid filename parsing."""
    with pytest.raises(ValueError):
        FileParser.parse_filename("invalid_filename.xlsx")

