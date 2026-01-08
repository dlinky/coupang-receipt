"""Mapping configuration data model."""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Condition:
    """Condition for conditional copy operations."""
    source_sheet: str
    name_column: str
    value_column: str
    check_column: str
    check_value: str


@dataclass
class MappingConfiguration:
    """Represents a data mapping rule."""
    data_name: str
    branch_sheet: str
    branch_range: str
    head_office_sheet: str
    head_office_range: str
    calculation_method: str
    condition: Optional[Condition] = None
    date_format: Optional[str] = None
    date_type: Optional[str] = None
    sort_column: Optional[str] = None
    sort_order: Optional[str] = None
    fee_ratio: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MappingConfiguration":
        """Create MappingConfiguration from dictionary."""
        condition = None
        if "condition" in data and data["condition"]:
            condition = Condition(**data["condition"])
        
        return cls(
            data_name=data["data_name"],
            branch_sheet=data["branch_sheet"],
            branch_range=data["branch_range"],
            head_office_sheet=data["head_office_sheet"],
            head_office_range=data["head_office_range"],
            calculation_method=data["calculation_method"],
            condition=condition,
            date_format=data.get("date_format"),
            date_type=data.get("date_type"),
            sort_column=data.get("sort_column"),
            sort_order=data.get("sort_order"),
            fee_ratio=data.get("fee_ratio"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert MappingConfiguration to dictionary."""
        result = {
            "data_name": self.data_name,
            "branch_sheet": self.branch_sheet,
            "branch_range": self.branch_range,
            "head_office_sheet": self.head_office_sheet,
            "head_office_range": self.head_office_range,
            "calculation_method": self.calculation_method,
        }
        
        if self.condition:
            result["condition"] = {
                "source_sheet": self.condition.source_sheet,
                "name_column": self.condition.name_column,
                "value_column": self.condition.value_column,
                "check_column": self.condition.check_column,
                "check_value": self.condition.check_value,
            }
        
        if self.date_format:
            result["date_format"] = self.date_format
        
        if self.date_type:
            result["date_type"] = self.date_type
        
        if self.sort_column:
            result["sort_column"] = self.sort_column
        
        if self.sort_order:
            result["sort_order"] = self.sort_order
        
        if self.fee_ratio is not None:
            result["fee_ratio"] = self.fee_ratio
        
        return result

