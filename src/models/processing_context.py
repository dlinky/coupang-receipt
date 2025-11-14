"""Processing context data model."""

from dataclasses import dataclass, field
from typing import List, Optional
from .file_info import FileInformation


@dataclass
class ProcessingContext:
    """Represents the current mapping operation state."""
    selected_weeks: List[int]
    head_office_file: FileInformation
    branch_file_path: str
    current_week: Optional[int] = None
    current_mapping: Optional[str] = None
    progress: float = 0.0
    status: str = "idle"
    error_message: Optional[str] = None
    error_type: Optional[str] = None

    def validate(self) -> None:
        """Validate processing context."""
        if not self.selected_weeks:
            raise ValueError("Selected weeks cannot be empty")
        for week in self.selected_weeks:
            if not (1 <= week <= 5):
                raise ValueError(f"Week must be between 1 and 5, got {week}")
        if self.status == "error" and not self.error_message:
            raise ValueError("Error message is required when status is 'error'")

    def start_processing(self) -> None:
        """Start processing operation."""
        self.status = "processing"
        self.progress = 0.0
        self.error_message = None
        self.error_type = None

    def update_progress(self, progress: float) -> None:
        """Update processing progress."""
        if not (0.0 <= progress <= 1.0):
            raise ValueError(f"Progress must be between 0.0 and 1.0, got {progress}")
        self.progress = progress

    def complete(self) -> None:
        """Mark processing as complete."""
        self.status = "completed"
        self.progress = 1.0

    def set_error(self, error_message: str, error_type: str) -> None:
        """Set error state."""
        self.status = "error"
        self.error_message = error_message
        self.error_type = error_type

