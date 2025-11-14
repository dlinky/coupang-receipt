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

