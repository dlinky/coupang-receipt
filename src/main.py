"""Main entry point for settlement automation application."""

import sys
from pathlib import Path

# Add parent directory to path for absolute imports
# This allows the script to work when run directly or as a PyInstaller bundle
# Get the directory containing this file (src/)
src_dir = Path(__file__).parent
# Get the parent directory (project root)
project_root = src_dir.parent
# Add project root to sys.path if not already there
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication
from src.gui.main_window import MainWindow
from src.logger import setup_logging


def main():
    """Main application entry point."""
    logger = setup_logging()
    logger.info("Starting settlement automation application")
    
    app = QApplication(sys.argv)
    app.setApplicationName("본사 정산서 자동화")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

