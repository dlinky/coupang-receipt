"""Main entry point for settlement automation application."""

import sys
from PySide6.QtWidgets import QApplication
from .gui.main_window import MainWindow
from .logger import setup_logging


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

