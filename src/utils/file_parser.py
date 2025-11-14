"""File name parser utility."""

import re
from pathlib import Path
from ..models.file_info import FileInformation


class FileParser:
    """Parses file names to extract year, month, and week information."""
    
    PATTERN = re.compile(r"빅보스_부산_진구중앙_(\d{4})_(\d{1,2})-(\d)\.xlsx")
    
    @classmethod
    def parse_filename(cls, file_path: str) -> FileInformation:
        """Parse filename to extract file information."""
        path = Path(file_path)
        filename = path.name
        
        match = cls.PATTERN.match(filename)
        if not match:
            raise ValueError(
                f"Filename does not match expected pattern: {filename}. "
                "Expected format: 빅보스_부산_진구중앙_YYYY_MM-W.xlsx"
            )
        
        year = int(match.group(1))
        month = int(match.group(2))
        week = int(match.group(3))
        
        file_info = FileInformation(
            file_path=str(path.absolute()),
            year=year,
            month=month,
            week=week,
            is_protected=False
        )
        file_info.validate()
        
        return file_info
    
    @classmethod
    def generate_branch_filename(cls, year: int, month: int, week: int) -> str:
        """Generate branch file name from year, month, week."""
        return f"쿠팡 {month}월 {week}주차 정산표.xlsx"

