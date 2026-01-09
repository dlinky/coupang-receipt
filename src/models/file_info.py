"""File information data model."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class FileInformation:
    """Represents parsed information from head office file."""
    file_path: str
    year: int
    month: int
    week: int
    password: Optional[str] = None
    is_protected: bool = False

    def validate(self) -> None:
        """Validate file information."""
        if not (2000 <= self.year <= 2100):
            raise ValueError(f"Year must be between 2000 and 2100, got {self.year}")
        if not (1 <= self.month <= 12):
            raise ValueError(f"Month must be between 1 and 12, got {self.month}")
        if not (1 <= self.week <= 8):
            raise ValueError(f"Week must be between 1 and 8, got {self.week}")
        if self.is_protected and not self.password:
            raise ValueError("Password is required for protected files")

