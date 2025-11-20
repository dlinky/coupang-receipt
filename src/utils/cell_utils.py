"""Cell utility functions."""

import re
from typing import Tuple, Optional, List
from openpyxl.utils import get_column_letter, column_index_from_string


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
    
    @classmethod
    def parse_multiple_ranges(cls, ranges_str: str) -> List[str]:
        """Parse comma-separated cell ranges.
        
        Args:
            ranges_str: Comma-separated cell ranges like "G17:I46" or "K17:K46, M17:M46, O17:O46"
        
        Returns:
            List of individual cell range strings
        
        Raises:
            ValueError: If any range format is invalid
        
        Examples:
            >>> CellUtils.parse_multiple_ranges("G17:I46")
            ['G17:I46']
            >>> CellUtils.parse_multiple_ranges("K17:K46, M17:M46, O17:O46")
            ['K17:K46', 'M17:M46', 'O17:O46']
        """
        if not ranges_str or not ranges_str.strip():
            raise ValueError("Empty ranges string")
        
        # Split by comma and strip whitespace
        ranges = [r.strip() for r in ranges_str.split(",")]
        
        # Validate each range
        for range_str in ranges:
            if not range_str:
                raise ValueError(f"Empty range found in: {ranges_str}")
            # Validate by trying to parse it
            cls.parse_range(range_str)
        
        return ranges
    
    @classmethod
    def increment_column(cls, column: str, offset: int = 1) -> str:
        """Increment Excel column letter.
        
        Args:
            column: Column letter like "A", "F", "Z", "AA"
            offset: Number of columns to increment (default: 1)
        
        Returns:
            Incremented column letter
        
        Examples:
            >>> CellUtils.increment_column("F")
            'G'
            >>> CellUtils.increment_column("Z")
            'AA'
            >>> CellUtils.increment_column("AA")
            'AB'
        """
        col_idx = column_index_from_string(column)
        new_col_idx = col_idx + offset
        return get_column_letter(new_col_idx)
    
    @classmethod
    def increment_column_in_range(cls, cell_range: str, offset: int = 1) -> str:
        """Increment column letters in cell range.
        
        Args:
            cell_range: Cell range like "F6:F35" or "AJ4"
            offset: Number of columns to increment (default: 1)
        
        Returns:
            Updated cell range with incremented columns
        
        Examples:
            >>> CellUtils.increment_column_in_range("F6:F35")
            'G6:G35'
            >>> CellUtils.increment_column_in_range("AJ4")
            'AK4'
        """
        if offset == 0:
            return cell_range
        
        start_col, start_row, end_col, end_row = cls.parse_range(cell_range)
        
        new_start_col = cls.increment_column(start_col, offset)
        new_end_col = cls.increment_column(end_col, offset)
        
        if ":" in cell_range:
            return f"{new_start_col}{start_row}:{new_end_col}{end_row}"
        else:
            return f"{new_start_col}{start_row}"

