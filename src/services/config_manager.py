"""Configuration manager service."""

import json
import os
from pathlib import Path
from typing import Dict, Any, List
from ..models.mapping_config import MappingConfiguration


class ConfigManager:
    """Manages application configuration and mapping settings."""
    
    def __init__(self, config_path: str = "config/config.json", 
                 mapping_path: str = "config/mapping.json"):
        """Initialize config manager."""
        self.config_path = Path(config_path)
        self.mapping_path = Path(mapping_path)
        self._config: Dict[str, Any] = {}
        self._mappings: List[MappingConfiguration] = []
    
    def load_config(self) -> Dict[str, Any]:
        """Load application configuration."""
        if not self.config_path.exists():
            return self._get_default_config()
        
        with open(self.config_path, "r", encoding="utf-8") as f:
            self._config = json.load(f)
        
        return self._config
    
    def save_config(self, config: Dict[str, Any]) -> None:
        """Save application configuration."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        self._config = config
    
    def load_mappings(self) -> List[MappingConfiguration]:
        """Load mapping configurations."""
        if not self.mapping_path.exists():
            return []
        
        with open(self.mapping_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self._mappings = [
            MappingConfiguration.from_dict(item) 
            for item in data
        ]
        return self._mappings
    
    def save_mappings(self, mappings: List[MappingConfiguration]) -> None:
        """Save mapping configurations."""
        self.mapping_path.parent.mkdir(parents=True, exist_ok=True)
        data = [mapping.to_dict() for mapping in mappings]
        with open(self.mapping_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        self._mappings = mappings
    
    def get_default_password(self) -> str:
        """Get default password from config."""
        config = self.load_config()
        return config.get("default_password", "4880403942")
    
    def get_week_offset(self, week: int) -> int:
        """Get week offset from config."""
        config = self.load_config()
        week_offsets = config.get("week_offsets", {})
        return week_offsets.get(str(week), 0)
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "default_password": "4880403942",
            "week_offsets": {
                "1": 0,
                "2": 36,
                "3": 72,
                "4": 108,
                "5": 144
            },
            "mapping_file_path": "config/mapping.json",
            "config_file_path": "config/config.json"
        }

