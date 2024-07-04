import os
from typing import List, Dict

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget, QMessageBox

from .FileItemWidget import FileItemWidget


class FileListWidget(QWidget):
    DISPLAY_LIMIT = 3  # 界面显示给用户的文件数量
    fileChanged = pyqtSignal(int)

    def __init__(self):
        """
        文件列表组件
        """
        super().__init__()
        self._file_paths: List[str] = []  # 全部文件列表
        self._file_paths_dic: Dict[str, FileItemWidget] = {}  # 正在处理的文件
        self.init_ui()

    def init_ui(self):
        self.grid_layout = QGridLayout()
        self.add_title()
        self.setLayout(self.grid_layout)
        self.setFixedHeight(150)

    def add_title(self):
        """添加表格的标题栏"""
        self.grid_layout.addWidget(QLabel('文件名'), 0, 0)
        self.grid_layout.addWidget(QLabel('文件大小'), 0, 1)
        self.grid_layout.addWidget(QLabel('进度'), 0, 2)

    def add_files(self, file_paths: List[str]):
        valid_files = []
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            if file_path and os.path.exists(file_path) and file_path not in self._file_paths:
                valid_files.append(file_path)
            else:
                QMessageBox.warning(self, "错误", f"{file_name} 不是有效的文件")
        if valid_files:
            self._file_paths.extend(valid_files)
            self.populate_file_list()

    def populate_file_list(self):
        """刷新文件列表，移除已完成的文件，添加新文件"""
        for file_path in list(self._file_paths_dic.keys()):
            file_item = self._file_paths_dic[file_path]
            if file_item.is_complete():
                self._file_paths_dic.pop(file_path)
                self.grid_layout.removeWidget(file_item)
                file_item.deleteLater()
        for file_path in self._file_paths[:self.DISPLAY_LIMIT]:
            if file_path not in self._file_paths_dic:
                file_item = FileItemWidget(file_path)
                if not file_item.is_complete():
                    num_rows = self.grid_layout.rowCount()
                    self.grid_layout.addWidget(file_item, num_rows, 0, 1, 3)
                    self._file_paths_dic[file_path] = file_item
        if len(self._file_paths) > self.DISPLAY_LIMIT:
            self.grid_layout.addWidget(QLabel(f'还剩下{len(self._file_paths) - self.DISPLAY_LIMIT}个文件待处理'),
                                       self.DISPLAY_LIMIT + 1, 0, 1, 3)

    def set_progress(self, file_path: str, progress_value: int):
        if file_path in self._file_paths_dic:
            self._file_paths_dic[file_path].set_progress(progress_value)
        if progress_value == 100:
            self._file_paths.remove(file_path)
            self.populate_file_list()
            self.fileChanged.emit(len(self._file_paths))

    def get_file_paths(self):
        return self._file_paths

    def get_file_paths_dic(self):
        return self._file_paths_dic
