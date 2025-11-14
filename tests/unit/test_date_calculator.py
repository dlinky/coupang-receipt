"""Unit tests for date calculator."""

import pytest
from datetime import datetime
from src.services.date_calculator import DateCalculator


def test_calculate_title_date():
    """Test title date calculation."""
    result = DateCalculator.calculate_title_date(2024, 11, 1)
    assert result == "11월 1주차"


def test_calculate_payment_date():
    """Test payment date calculation."""
    result = DateCalculator.calculate_payment_date(2024, 11, 1)
    assert result.startswith("24.11.")
    assert len(result) == 8


def test_calculate_date_range():
    """Test date range calculation."""
    result = DateCalculator.calculate_date_range(2024, 11, 1)
    assert " ~ " in result
    assert len(result.split(" ~ ")) == 2

