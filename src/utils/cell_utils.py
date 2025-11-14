"""Cell utility functions."""

import re
from typing import Tuple, Optional


class CellUtils:
    """Utility functions for cell range parsing and manipulation."""
    
    CELL_PATTERN = re.compile(r"([A-Z]+)(\d+)")
    RANGE_PATTERN = re.compile(r"([A-Z]+\d+):([A-Z]+\d+)")
    
    @classmethod
    def parse_cell(cls, cell_address: str) -> Tuple[str, int]:
        """Parse cell address to column and row.
        
        Args:
            cell_address: Cell address like "A1" or "C6"
        
        Returns:
            Tuple of (column, row) where column is string and row is int
        """
        match = cls.CELL_PATTERN.match(cell_address)
        if not match:
            raise ValueError(f"Invalid cell address format: {cell_address}")
        
        column = match.group(1)
        row = int(match.group(2))
        return (column, row)
    
    @classmethod
    def parse_range(cls, cell_range: str) -> Tuple[str, int, str, int]:
        """Parse cell range to start and end cells.
        
        Args:
            cell_range: Cell range like "A1:B10" or "C6:C35"
        
        Returns:
            Tuple of (start_column, start_row, end_column, end_row)
        """
        if ":" not in cell_range:
            column, row = cls.parse_cell(cell_range)
            return (column, row, column, row)
        
        match = cls.RANGE_PATTERN.match(cell_range)
        if not match:
            raise ValueError(f"Invalid cell range format: {cell_range}")
        
        start_cell = match.group(1)
        end_cell = match.group(2)
        
        start_col, start_row = cls.parse_cell(start_cell)
        end_col, end_row = cls.parse_cell(end_cell)
        
        return (start_col, start_row, end_col, end_row)
    
    @classmethod
    def apply_row_offset(cls, cell_range: str, offset: int) -> str:
        """Apply row offset to cell range.
        
        Args:
            cell_range: Cell range like "C6:C35"
            offset: Row offset to apply
        
        Returns:
            Updated cell range with offset applied
        """
        if offset == 0:
            return cell_range
        
        start_col, start_row, end_col, end_row = cls.parse_range(cell_range)
        
        new_start_row = start_row + offset
        new_end_row = end_row + offset
        
        if ":" in cell_range:
            return f"{start_col}{new_start_row}:{end_col}{new_end_row}"
        else:
            return f"{start_col}{new_start_row}"
    
    @classmethod
    def format_cell(cls, column: str, row: int) -> str:
        """Format column and row to cell address."""
        return f"{column}{row}"
    
    @classmethod
    def apply_week_offset(cls, cell_range: str, week: int, week_offsets: dict) -> str:
        """Apply week offset to cell range.
        
        Args:
            cell_range: Cell range like "C6:C35"
            week: Week number (1-5)
            week_offsets: Dictionary mapping week to offset
        
        Returns:
            Updated cell range with offset applied
        """
        offset = week_offsets.get(str(week), 0)
        return cls.apply_row_offset(cell_range, offset)

