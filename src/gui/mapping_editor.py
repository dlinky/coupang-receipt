"""Mapping editor window GUI."""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView
)
from typing import List
from ..models.mapping_config import MappingConfiguration
from ..services.config_manager import ConfigManager


class MappingEditor(QDialog):
    """Mapping configuration editor window."""
    
    def __init__(self, parent=None):
        """Initialize mapping editor."""
        super().__init__(parent)
        self.config_manager = ConfigManager()
        self.mappings: List[MappingConfiguration] = []
        self.init_ui()
        self.load_mappings()
    
    def init_ui(self):
        """Initialize UI components."""
        self.setWindowTitle("매핑 설정 수정")
        self.setGeometry(200, 200, 1000, 600)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "데이터 이름", "지점 시트", "지점 범위",
            "본사 시트", "본사 범위", "계산 방식"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("추가")
        add_btn.clicked.connect(self.add_mapping)
        button_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("수정")
        edit_btn.clicked.connect(self.edit_mapping)
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("삭제")
        delete_btn.clicked.connect(self.delete_mapping)
        button_layout.addWidget(delete_btn)
        
        button_layout.addStretch()
        
        save_btn = QPushButton("저장")
        save_btn.clicked.connect(self.save_mappings)
        button_layout.addWidget(save_btn)
        
        close_btn = QPushButton("닫기")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
    
    def load_mappings(self):
        """Load mappings from config."""
        self.mappings = self.config_manager.load_mappings()
        self.update_table()
    
    def update_table(self):
        """Update table with current mappings."""
        self.table.setRowCount(len(self.mappings))
        
        for row, mapping in enumerate(self.mappings):
            self.table.setItem(row, 0, QTableWidgetItem(mapping.data_name))
            self.table.setItem(row, 1, QTableWidgetItem(mapping.branch_sheet))
            self.table.setItem(row, 2, QTableWidgetItem(mapping.branch_range))
            self.table.setItem(row, 3, QTableWidgetItem(mapping.head_office_sheet))
            self.table.setItem(row, 4, QTableWidgetItem(mapping.head_office_range))
            self.table.setItem(row, 5, QTableWidgetItem(mapping.calculation_method))
    
    def add_mapping(self):
        """Add new mapping (placeholder)."""
        QMessageBox.information(
            self,
            "알림",
            "새 매핑 추가 기능은 향후 구현 예정입니다."
        )
    
    def edit_mapping(self):
        """Edit selected mapping (placeholder)."""
        QMessageBox.information(
            self,
            "알림",
            "매핑 수정 기능은 향후 구현 예정입니다."
        )
    
    def delete_mapping(self):
        """Delete selected mapping."""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "경고", "삭제할 항목을 선택해주세요.")
            return
        
        reply = QMessageBox.question(
            self,
            "확인",
            f"'{self.mappings[current_row].data_name}' 매핑을 삭제하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.mappings.pop(current_row)
            self.update_table()
    
    def save_mappings(self):
        """Save mappings to config."""
        try:
            self.config_manager.save_mappings(self.mappings)
            QMessageBox.information(self, "완료", "매핑 설정이 저장되었습니다.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "오류", f"저장 실패: {e}")

