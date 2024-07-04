import os

from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget, QProgressBar, QMessageBox


class FileItemWidget(QWidget):
    def __init__(self, file_path: str):
        """
        文件列表中的文件项组件

        :param file_path: 文件路径
        :type file_path: str
        """
        super().__init__()
        self.file_path = file_path

        self.grid_layout = QGridLayout()
        file_name = os.path.basename(file_path)
        self._file_name_label = QLabel(file_name)

        try:
            file_size = os.path.getsize(file_path)
            self._file_size_label = QLabel(self.format_size(file_size))
        except FileNotFoundError:
            self._file_size_label = QLabel("文件不存在")
            QMessageBox.warning(self, "错误", f"文件未找到: {file_path}")

        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(0)

        self.grid_layout.addWidget(self._file_name_label, 0, 0)
        self.grid_layout.addWidget(self._file_size_label, 0, 1)
        self.grid_layout.addWidget(self._progress_bar, 0, 2)

        self.grid_layout.setColumnStretch(0, 4)
        self.grid_layout.setColumnStretch(1, 4)
        self.grid_layout.setColumnStretch(2, 6)

        self.setLayout(self.grid_layout)

    @staticmethod
    def format_size(size: float):
        # 将文件大小格式化为人类可读的字符串
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                break
            size /= 1024.0
        return "{:.2f} {}".format(size, unit)

    def set_progress(self, progress_value: int):
        self._progress_bar.setValue(progress_value)

    def is_complete(self):
        return self._progress_bar.value() == 100
