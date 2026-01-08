"""Main window GUI."""

import sys
from pathlib import Path
from typing import Optional
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QProgressBar,
    QTextEdit, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QCheckBox
)
from PySide6.QtCore import Qt, QThread, Signal

from ..models.file_info import FileInformation
from ..models.processing_context import ProcessingContext
from ..services.mapping_engine import MappingEngine
from ..services.config_manager import ConfigManager
from ..utils.file_parser import FileParser
from ..exceptions import FileError, MappingError
from ..logger import setup_logging


class MappingWorker(QThread):
    """Worker thread for mapping operations."""
    
    progress_updated = Signal(float, str)
    completed = Signal(bool, str)
    
    def __init__(self, context: ProcessingContext, mapping_engine: MappingEngine):
        """Initialize worker."""
        super().__init__()
        self.context = context
        self.mapping_engine = mapping_engine
    
    def run(self):
        """Execute mapping in background thread."""
        try:
            from openpyxl import Workbook
            from ..services.excel_processor import ExcelProcessor
            
            self.context.start_processing()
            mappings = self.mapping_engine.load_mappings()
            weekly_mappings = [m for m in mappings if m.calculation_method != "unique_extraction"]
            monthly_mappings = [m for m in mappings if m.calculation_method == "unique_extraction"]
            total_weeks = len(self.context.selected_weeks)
            total_tasks = total_weeks * len(weekly_mappings) + len(monthly_mappings)
            
            # Check if there are any mappings to process
            if total_tasks == 0:
                self.completed.emit(False, "매핑 설정이 없습니다. 매핑 설정 파일을 확인해주세요.")
                return
            
            # Check if weeks are selected
            if total_weeks == 0:
                self.completed.emit(False, "주차가 선택되지 않았습니다.")
                return
            
            completed_tasks = 0
            
            excel_processor = ExcelProcessor()
            branch_workbook = excel_processor.load_workbook(
                self.context.branch_file_path, data_only=False
            )
            
            for week in self.context.selected_weeks:
                self.context.current_week = week
                progress = completed_tasks / total_tasks if total_tasks > 0 else 0.0
                self.progress_updated.emit(
                    progress,
                    f"Processing week {week}..."
                )
                
                for mapping in weekly_mappings:
                    result = self.mapping_engine.execute_mapping(
                        mapping,
                        self.context.head_office_file,
                        self.context.branch_file_path,
                        week,
                        branch_workbook
                    )
                    
                    if not result.success:
                        self.completed.emit(False, result.error_message or "Mapping failed")
                        return
                    
                    completed_tasks += 1
                    progress = completed_tasks / total_tasks if total_tasks > 0 else 1.0
                    self.progress_updated.emit(
                        progress,
                        f"Completed: {mapping.data_name} (Week {week})"
                    )
            
            for mapping in monthly_mappings:
                result = self.mapping_engine.execute_mapping(
                    mapping,
                    self.context.head_office_file,
                    self.context.branch_file_path,
                    1,
                    branch_workbook
                )
                
                if not result.success:
                    self.completed.emit(False, result.error_message or "Mapping failed")
                    return
                
                completed_tasks += 1
                progress = completed_tasks / total_tasks if total_tasks > 0 else 1.0
                self.progress_updated.emit(
                    progress,
                    f"Completed: {mapping.data_name}"
                )
            
            first_week = self.context.selected_weeks[0]
            new_file_path = self.mapping_engine.save_branch_file(
                branch_workbook,
                self.context.branch_file_path,
                self.context.head_office_file,
                first_week
            )
            
            self.context.complete()
            self.completed.emit(True, f"Mapping completed successfully. Saved to: {Path(new_file_path).name}")
            
        except Exception as e:
            self.context.set_error(str(e), "system_error")
            self.completed.emit(False, f"Error: {e}")


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        """Initialize main window."""
        super().__init__()
        self.config_manager = ConfigManager()
        self.mapping_engine = MappingEngine(self.config_manager)
        self.logger = setup_logging()
        
        self.head_office_file: Optional[FileInformation] = None
        self.branch_file_path: Optional[str] = None
        self.worker: Optional[MappingWorker] = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI components."""
        self.setWindowTitle("본사 정산서 자동화 프로그램")
        self.setGeometry(100, 100, 1200, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main horizontal layout (left: controls, right: fee table)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Left side: controls
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        
        # Head office file selection
        head_office_layout = QHBoxLayout()
        head_office_label = QLabel("본사 파일:")
        self.head_office_path_label = QLabel("선택되지 않음")
        self.head_office_path_label.setWordWrap(True)
        head_office_btn = QPushButton("본사 파일 선택")
        head_office_btn.clicked.connect(self.select_head_office_file)
        head_office_layout.addWidget(head_office_label)
        head_office_layout.addWidget(self.head_office_path_label, 1)
        head_office_layout.addWidget(head_office_btn)
        left_layout.addLayout(head_office_layout)
        
        # Password input
        password_layout = QHBoxLayout()
        password_label = QLabel("비밀번호:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setText(self.config_manager.get_default_password())
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input, 1)
        left_layout.addLayout(password_layout)
        
        # Branch file selection
        branch_layout = QHBoxLayout()
        branch_label = QLabel("지점 파일:")
        self.branch_path_label = QLabel("선택되지 않음")
        self.branch_path_label.setWordWrap(True)
        branch_btn = QPushButton("지점 파일 선택")
        branch_btn.clicked.connect(self.select_branch_file)
        branch_layout.addWidget(branch_label)
        branch_layout.addWidget(self.branch_path_label, 1)
        branch_layout.addWidget(branch_btn)
        left_layout.addLayout(branch_layout)
        
        # Week selection
        week_layout = QHBoxLayout()
        week_label = QLabel("주차 선택:")
        self.week_combo = QComboBox()
        self.week_combo.addItems(["1주차", "2주차", "3주차", "4주차", "5주차", "전체"])
        week_layout.addWidget(week_label)
        week_layout.addWidget(self.week_combo, 1)
        left_layout.addLayout(week_layout)
        
        # Execute button
        execute_btn = QPushButton("작업 시작")
        execute_btn.clicked.connect(self.execute_mapping)
        left_layout.addWidget(execute_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        left_layout.addWidget(self.progress_bar)
        
        # Log output
        log_label = QLabel("진행 상황:")
        left_layout.addWidget(log_label)
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        left_layout.addWidget(self.log_output, 1)
        
        # Mapping editor button
        editor_btn = QPushButton("매핑 설정 수정")
        editor_btn.clicked.connect(self.open_mapping_editor)
        left_layout.addWidget(editor_btn)
        
        # Right side: Fee table
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        
        fee_label = QLabel("수수료 적용")
        right_layout.addWidget(fee_label)
        
        # Create table with 2 columns: 성함, 수수료 적용
        self.fee_table = QTableWidget()
        self.fee_table.setColumnCount(2)
        self.fee_table.setHorizontalHeaderLabels(["성함", "수수료 적용"])
        self.fee_table.horizontalHeader().setStretchLastSection(True)
        self.fee_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.fee_table.verticalHeader().setVisible(False)
        right_layout.addWidget(self.fee_table)
        
        # Add widgets to main layout
        main_layout.addWidget(left_widget, 2)
        main_layout.addWidget(right_widget, 1)
    
    def select_head_office_file(self):
        """Select head office file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "본사 정산서 파일 선택",
            "",
            "Excel Files (*.xlsx)"
        )
        
        if file_path:
            try:
                if not Path(file_path).exists():
                    QMessageBox.critical(self, "오류", "파일이 존재하지 않습니다.")
                    return
                
                if not file_path.endswith('.xlsx'):
                    QMessageBox.critical(self, "오류", "Excel 파일(.xlsx)만 지원됩니다.")
                    return
                
                self.head_office_file = FileParser.parse_filename(file_path)
                self.head_office_file.password = self.password_input.text() or None
                self.head_office_file.is_protected = bool(self.password_input.text())
                self.head_office_path_label.setText(Path(file_path).name)
                self.log_output.append(f"본사 파일 로드: {Path(file_path).name}")
                self.logger.info(f"Head office file loaded: {file_path}")
                
                # Load rider names from head office file
                self.load_rider_names()
            except ValueError as e:
                QMessageBox.critical(
                    self,
                    "파일명 형식 오류",
                    f"파일명 형식이 올바르지 않습니다.\n\n"
                    f"예상 형식: 빅보스_부산_진구중앙_YYYY_MM-W.xlsx\n"
                    f"오류: {e}\n\n"
                    f"수동으로 월과 주차를 입력하시겠습니까?"
                )
                self.logger.error(f"Failed to parse filename: {e}")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"파일 로드 실패: {e}")
                self.logger.error(f"Failed to load head office file: {e}")
    
    def select_branch_file(self):
        """Select branch file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "지점 정산서 파일 선택",
            "",
            "Excel Files (*.xlsx)"
        )
        
        if file_path:
            self.branch_file_path = file_path
            self.branch_path_label.setText(Path(file_path).name)
            self.log_output.append(f"지점 파일 선택: {Path(file_path).name}")
            self.logger.info(f"Branch file selected: {file_path}")
    
    def execute_mapping(self):
        """Execute mapping operation."""
        if not self.head_office_file:
            QMessageBox.warning(self, "경고", "본사 파일을 선택해주세요.")
            return
        
        if not self.branch_file_path:
            QMessageBox.warning(self, "경고", "지점 파일을 선택해주세요.")
            return
        
        if not Path(self.branch_file_path).exists():
            QMessageBox.critical(self, "오류", "지점 파일이 존재하지 않습니다.")
            return
        
        week_text = self.week_combo.currentText()
        if week_text == "전체":
            selected_weeks = [1, 2, 3, 4, 5]
        else:
            selected_weeks = [int(week_text[0])]
        
        context = ProcessingContext(
            selected_weeks=selected_weeks,
            head_office_file=self.head_office_file,
            branch_file_path=self.branch_file_path
        )
        
        self.worker = MappingWorker(context, self.mapping_engine)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.completed.connect(self.mapping_completed)
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.log_output.append("매핑 시작...")
        
        self.worker.start()
    
    def update_progress(self, progress: float, message: str):
        """Update progress bar and log."""
        self.progress_bar.setValue(int(progress * 100))
        self.log_output.append(message)
    
    def mapping_completed(self, success: bool, message: str):
        """Handle mapping completion."""
        self.progress_bar.setVisible(False)
        
        if success:
            QMessageBox.information(self, "완료", message)
            self.log_output.append("매핑 완료!")
            self.logger.info("Mapping completed successfully")
        else:
            error_msg = f"매핑 실행 중 오류가 발생했습니다.\n\n{message}"
            
            if "Sheet" in message or "시트" in message:
                error_msg += "\n\n매핑 설정 파일을 확인하시겠습니까?"
                reply = QMessageBox.critical(
                    self,
                    "매핑 오류",
                    error_msg,
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    import subprocess
                    import platform
                    mapping_file = self.config_manager.mapping_path
                    if platform.system() == "Windows":
                        subprocess.Popen(["notepad.exe", str(mapping_file)])
                    elif platform.system() == "Darwin":
                        subprocess.Popen(["open", "-a", "TextEdit", str(mapping_file)])
                    else:
                        subprocess.Popen(["xdg-open", str(mapping_file)])
            else:
                QMessageBox.critical(self, "오류", error_msg)
            
            self.log_output.append(f"오류: {message}")
            self.logger.error(f"Mapping failed: {message}")
    
    def load_rider_names(self):
        """Load rider names from head office file and populate fee table."""
        if not self.head_office_file:
            return
        
        try:
            from ..services.excel_processor import ExcelProcessor
            
            excel_processor = ExcelProcessor()
            head_workbook = excel_processor.load_workbook(
                self.head_office_file.file_path,
                self.head_office_file.password
            )
            
            # Find mapping for "성함" (rider names)
            mappings = self.mapping_engine.load_mappings()
            name_mapping = None
            for mapping in mappings:
                if mapping.data_name == "성함":
                    name_mapping = mapping
                    break
            
            if not name_mapping:
                self.log_output.append("경고: '성함' 매핑 설정을 찾을 수 없습니다.")
                return
            
            head_sheet = excel_processor.get_sheet(head_workbook, name_mapping.head_office_sheet)
            rider_names = excel_processor.read_cell_range(head_sheet, name_mapping.head_office_range)
            
            # Load saved fee riders
            saved_fee_riders = self.config_manager.get_fee_riders()
            
            # Populate table
            self.fee_table.setRowCount(len(rider_names))
            for i, name in enumerate(rider_names):
                if name and str(name).strip():
                    # Name column
                    name_item = QTableWidgetItem(str(name).strip())
                    name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
                    self.fee_table.setItem(i, 0, name_item)
                    
                    # Checkbox column
                    checkbox = QCheckBox()
                    checkbox.setChecked(str(name).strip() in saved_fee_riders)
                    checkbox.stateChanged.connect(self.on_fee_checkbox_changed)
                    self.fee_table.setCellWidget(i, 1, checkbox)
            
            self.log_output.append(f"배달기사 목록 로드 완료: {len([n for n in rider_names if n])}명")
            
        except Exception as e:
            self.log_output.append(f"배달기사 목록 로드 실패: {e}")
            self.logger.error(f"Failed to load rider names: {e}")
    
    def on_fee_checkbox_changed(self):
        """Handle fee checkbox state change and save to config."""
        fee_riders = []
        for i in range(self.fee_table.rowCount()):
            name_item = self.fee_table.item(i, 0)
            checkbox = self.fee_table.cellWidget(i, 1)
            if name_item and checkbox and checkbox.isChecked():
                fee_riders.append(name_item.text())
        
        self.config_manager.save_fee_riders(fee_riders)
    
    def get_fee_riders(self) -> list:
        """Get list of riders who have fee applied."""
        fee_riders = []
        for i in range(self.fee_table.rowCount()):
            name_item = self.fee_table.item(i, 0)
            checkbox = self.fee_table.cellWidget(i, 1)
            if name_item and checkbox and checkbox.isChecked():
                fee_riders.append(name_item.text())
        return fee_riders
    
    def open_mapping_editor(self):
        """Open mapping editor window."""
        from .mapping_editor import MappingEditor
        editor = MappingEditor(self)
        if editor.exec():
            self.mapping_engine.load_mappings()

