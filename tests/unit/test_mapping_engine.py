"""Unit tests for mapping engine."""

import pytest
from openpyxl import Workbook
from src.services.mapping_engine import MappingEngine
from src.models.mapping_config import MappingConfiguration
from src.models.file_info import FileInformation
from src.services.config_manager import ConfigManager


def test_execute_simple_sum_adjacent_columns():
    """Test simple_sum with adjacent columns (G17:I46)."""
    # Create test workbooks
    head_workbook = Workbook()
    head_sheet = head_workbook.active
    head_sheet.title = "종합"
    
    # Fill test data: G17=10, H17=20, I17=30 (sum=60)
    #                 G18=5, H18=15, I18=25 (sum=45)
    head_sheet["G17"] = 10
    head_sheet["H17"] = 20
    head_sheet["I17"] = 30
    head_sheet["G18"] = 5
    head_sheet["H18"] = 15
    head_sheet["I18"] = 25
    
    branch_workbook = Workbook()
    branch_sheet = branch_workbook.create_sheet("주간정산")
    
    # Create mapping config
    mapping_config = MappingConfiguration(
        data_name="배달료",
        branch_sheet="주간정산",
        branch_range="E6:E7",
        head_office_sheet="종합",
        head_office_range="G17:I18",
        calculation_method="simple_sum"
    )
    
    # Execute mapping
    engine = MappingEngine()
    result = engine._execute_simple_sum(
        mapping_config, head_workbook, branch_workbook, week_offset=0
    )
    
    # Verify result
    assert result.success is True
    assert result.rows_processed == 2
    assert branch_sheet["E6"].value == 60  # 10+20+30
    assert branch_sheet["E7"].value == 45  # 5+15+25


def test_execute_simple_sum_non_adjacent_columns():
    """Test simple_sum with non-adjacent columns (K17:K18, M17:M18, O17:O18)."""
    # Create test workbooks
    head_workbook = Workbook()
    head_sheet = head_workbook.active
    head_sheet.title = "종합"
    
    # Fill test data
    head_sheet["K17"] = 10
    head_sheet["M17"] = 20
    head_sheet["O17"] = 30
    head_sheet["Q17"] = 40
    head_sheet["K18"] = 5
    head_sheet["M18"] = 15
    head_sheet["O18"] = 25
    head_sheet["Q18"] = 35
    
    branch_workbook = Workbook()
    branch_sheet = branch_workbook.create_sheet("주간정산")
    
    # Create mapping config
    mapping_config = MappingConfiguration(
        data_name="추가배달료",
        branch_sheet="주간정산",
        branch_range="E6:E7",
        head_office_sheet="종합",
        head_office_range="K17:K18, M17:M18, O17:O18, Q17:Q18",
        calculation_method="simple_sum"
    )
    
    # Execute mapping
    engine = MappingEngine()
    result = engine._execute_simple_sum(
        mapping_config, head_workbook, branch_workbook, week_offset=0
    )
    
    # Verify result
    assert result.success is True
    assert result.rows_processed == 2
    assert branch_sheet["E6"].value == 100  # 10+20+30+40
    assert branch_sheet["E7"].value == 80  # 5+15+25+35


def test_execute_simple_sum_with_empty_values():
    """Test simple_sum with None/empty values (should be ignored)."""
    # Create test workbooks
    head_workbook = Workbook()
    head_sheet = head_workbook.active
    head_sheet.title = "종합"
    
    # Fill test data with None values
    head_sheet["G17"] = 10
    head_sheet["H17"] = None
    head_sheet["I17"] = 20
    head_sheet["G18"] = ""
    head_sheet["H18"] = 15
    head_sheet["I18"] = 25
    
    branch_workbook = Workbook()
    branch_sheet = branch_workbook.create_sheet("주간정산")
    
    # Create mapping config
    mapping_config = MappingConfiguration(
        data_name="배달료",
        branch_sheet="주간정산",
        branch_range="E6:E7",
        head_office_sheet="종합",
        head_office_range="G17:I18",
        calculation_method="simple_sum"
    )
    
    # Execute mapping
    engine = MappingEngine()
    result = engine._execute_simple_sum(
        mapping_config, head_workbook, branch_workbook, week_offset=0
    )
    
    # Verify result (None and empty string should be ignored)
    assert result.success is True
    assert result.rows_processed == 2
    assert branch_sheet["E6"].value == 30  # 10+0+20 (None ignored)
    assert branch_sheet["E7"].value == 40  # 0+15+25 (empty string ignored)


def test_execute_simple_sum_with_week_offset():
    """Test simple_sum with week offset applied to branch file."""
    # Create test workbooks
    head_workbook = Workbook()
    head_sheet = head_workbook.active
    head_sheet.title = "종합"
    head_sheet["G17"] = 10
    head_sheet["H17"] = 20
    head_sheet["I17"] = 30
    
    branch_workbook = Workbook()
    branch_sheet = branch_workbook.create_sheet("주간정산")
    
    # Create mapping config
    mapping_config = MappingConfiguration(
        data_name="배달료",
        branch_sheet="주간정산",
        branch_range="E6:E6",  # Will be offset to E42
        head_office_sheet="종합",
        head_office_range="G17:I17",
        calculation_method="simple_sum"
    )
    
    # Execute mapping with offset (2주차 = +36)
    engine = MappingEngine()
    result = engine._execute_simple_sum(
        mapping_config, head_workbook, branch_workbook, week_offset=36
    )
    
    # Verify result (offset applied to target range)
    assert result.success is True
    assert result.rows_processed == 1
    assert branch_sheet["E42"].value == 60  # 10+20+30, written to E42 (E6+36)


def test_execute_simple_sum_mismatched_row_count():
    """Test simple_sum with mismatched row counts (should fail)."""
    # Create test workbooks
    head_workbook = Workbook()
    head_sheet = head_workbook.active
    head_sheet.title = "종합"
    head_sheet["G17"] = 10
    head_sheet["H17"] = 20
    head_sheet["G18"] = 5
    head_sheet["H18"] = 15
    
    branch_workbook = Workbook()
    branch_sheet = branch_workbook.create_sheet("주간정산")
    
    # Create mapping config with mismatched ranges
    mapping_config = MappingConfiguration(
        data_name="배달료",
        branch_sheet="주간정산",
        branch_range="E6:E7",
        head_office_sheet="종합",
        head_office_range="G17:H18, K17:K17",  # First has 2 rows, second has 1 row
        calculation_method="simple_sum"
    )
    
    # Execute mapping
    engine = MappingEngine()
    result = engine._execute_simple_sum(
        mapping_config, head_workbook, branch_workbook, week_offset=0
    )
    
    # Verify result (should fail)
    assert result.success is False
    assert "same number of rows" in result.error_message.lower()

