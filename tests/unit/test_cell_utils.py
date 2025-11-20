"""Unit tests for cell utilities."""

import pytest
from src.utils.cell_utils import CellUtils


def test_parse_cell():
    """Test cell parsing."""
    column, row = CellUtils.parse_cell("A1")
    assert column == "A"
    assert row == 1


def test_parse_range():
    """Test range parsing."""
    start_col, start_row, end_col, end_row = CellUtils.parse_range("A1:B10")
    assert start_col == "A"
    assert start_row == 1
    assert end_col == "B"
    assert end_row == 10


def test_apply_row_offset():
    """Test row offset application."""
    result = CellUtils.apply_row_offset("C6:C35", 36)
    assert result == "C42:C71"


def test_parse_multiple_ranges_single_range():
    """Test parsing single range."""
    ranges = CellUtils.parse_multiple_ranges("G17:I46")
    assert ranges == ["G17:I46"]


def test_parse_multiple_ranges_multiple_ranges():
    """Test parsing multiple comma-separated ranges."""
    ranges = CellUtils.parse_multiple_ranges("K17:K46, M17:M46, O17:O46")
    assert ranges == ["K17:K46", "M17:M46", "O17:O46"]


def test_parse_multiple_ranges_with_spaces():
    """Test parsing ranges with spaces around commas."""
    ranges = CellUtils.parse_multiple_ranges("K17:K46,  M17:M46  , O17:O46")
    assert ranges == ["K17:K46", "M17:M46", "O17:O46"]


def test_parse_multiple_ranges_adjacent_columns():
    """Test parsing adjacent column ranges."""
    ranges = CellUtils.parse_multiple_ranges("G17:I46")
    assert ranges == ["G17:I46"]


def test_parse_multiple_ranges_empty_string():
    """Test parsing empty string raises error."""
    with pytest.raises(ValueError, match="Empty ranges string"):
        CellUtils.parse_multiple_ranges("")


def test_parse_multiple_ranges_invalid_range():
    """Test parsing invalid range raises error."""
    with pytest.raises(ValueError):
        CellUtils.parse_multiple_ranges("INVALID")

