"""Configuration manager service."""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List
from ..models.mapping_config import MappingConfiguration


def _get_resource_path(relative_path: str) -> Path:
    """Get the absolute path to a resource file.
    
    Works for both development and PyInstaller bundle environments.
    Priority order:
    1. Directory where executable is located (allows user override)
    2. Current working directory
    3. Bundle directory (PyInstaller only, read-only)
    4. Relative path (fallback)
    """
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    if hasattr(sys, '_MEIPASS'):
        # Running as a PyInstaller bundle
        # First, try the directory where the executable is located
        # This allows users to override config files by placing them next to the exe
        if hasattr(sys, 'executable') and sys.executable:
            exe_dir = Path(sys.executable).parent
            exe_path = exe_dir / relative_path
            if exe_path.exists():
                return exe_path
            # Return exe_dir path even if it doesn't exist yet (for writing)
            # This ensures config files are saved next to the executable
            return exe_path
        
        # If not found next to exe, try bundle directory (read-only)
        bundle_path = Path(sys._MEIPASS) / relative_path
        if bundle_path.exists():
            return bundle_path
    
    # Running as a normal Python script
    # Try current working directory first
    cwd_path = Path.cwd() / relative_path
    if cwd_path.exists():
        return cwd_path
    
    # Try the directory where the script is located
    if hasattr(sys, 'executable') and sys.executable:
        script_dir = Path(sys.executable).parent
        script_path = script_dir / relative_path
        if script_path.exists():
            return script_path
    
    # Fall back to relative path from current working directory
    return Path(relative_path)


class ConfigManager:
    """Manages application configuration and mapping settings."""
    
    def __init__(self, config_path: str = "config/config.json", 
                 mapping_path: str = "config/mapping.json"):
        """Initialize config manager."""
        self.config_path = _get_resource_path(config_path)
        self.mapping_path = _get_resource_path(mapping_path)
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
    
    def get_fee_riders(self) -> List[str]:
        """Get list of riders who have fee applied."""
        config = self.load_config()
        return config.get("fee_riders", [])
    
    def save_fee_riders(self, riders: List[str]) -> None:
        """Save list of riders who have fee applied."""
        config = self.load_config()
        config["fee_riders"] = riders
        self.save_config(config)
    
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

