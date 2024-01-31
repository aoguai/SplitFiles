import os
import copy
from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget
from ui.FileItemWidget import FileItemWidget
from PyQt5.QtCore import pyqtSignal

class FileListWidget(QWidget):
    _file_paths: list[str] = [] # 全部文件列表
    _file_paths_dic: dict[str, FileItemWidget] = {} # 正在处理的文件
    DISPLAY_LIMIT = 3   # 界面显示给用户的文件数量
    fileChanged = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.grid_layout = QGridLayout()
        self.add_title()

        self.setLayout(self.grid_layout)
        self.setFixedHeight(150)

    # 添加表格的标题栏
    def add_title(self):
        self.grid_layout.addWidget(QLabel('文件名'), 0, 0)
        self.grid_layout.addWidget(QLabel('文件大小'), 0, 1)
        self.grid_layout.addWidget(QLabel('进度'), 0, 2)
    
    # 添加需要处理的文件路径
    def add_files(self, file_paths: list[str]):
        for file_path in file_paths:
            # 排除重复的文件路径
            if file_path in self._file_paths:
                continue
            
            file_name = os.path.basename(file_path)
            if not file_path or not os.path.exists(file_path):
                print(f"{file_name} 不是有效的文件")
                continue
            
            self._file_paths.append(file_path)
        self.populate_file_list()
        
    def populate_file_list(self):
        for file_path, file_item in copy.copy(self._file_paths_dic).items():
            if file_item.is_complete():
                self._file_paths_dic.pop(file_path)
                self.grid_layout.removeWidget(file_item)
                file_item.deleteLater()

        # 只取_file_paths的前3个元素进行添加
        for _, file_path in enumerate(self._file_paths[:self.DISPLAY_LIMIT]):
            # 添加子组件
            if file_path in self._file_paths_dic:
                continue
            file_item = FileItemWidget(file_path)
            if not file_item.is_complete():
                num_rows = self.grid_layout.rowCount()
                self.grid_layout.addWidget(file_item, num_rows, 0, 1, 3) 
                self._file_paths_dic[file_path] = file_item
            
        # if len(self._file_paths) > self.DISPLAY_LIMIT:
        #     self.grid_layout.addWidget(QLabel(f'还剩下{len(self._file_paths) - self.DISPLAY_LIMIT}个文件待处理'), self.DISPLAY_LIMIT + 1, 0)

    def set_progress(self, file_path: str, progress_value: int):
        if file_path in self._file_paths_dic:
            self._file_paths_dic[file_path].set_progress(progress_value)

        if progress_value == 100:
            self._file_paths.remove(file_path)
            self.populate_file_list()
            self.fileChanged.emit(1)

    def get_file_paths(self):
        return self._file_paths
    
    def get_file_paths_dic(self):
        return self._file_paths_dic
    