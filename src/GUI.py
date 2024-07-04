import base64
import os
import sys
from typing import Dict

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox, \
    QRadioButton, QButtonGroup, QComboBox
from SplitFiles import SplitFiles
from model.FileSignalData import FileSignalData
from ui.DragRectWidget import DragRectWidget
from ui.FileListWidget import FileListWidget


class SplitFileGUI(QWidget):
    _worker_dict: Dict[str, SplitFiles] = {}

    def __init__(self):
        """
        初始化 GUI 界面
        包括拖放文件支持、进度条、输入字段、文本提示、按钮、布局和窗口属性的设置。
        """
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 支持拖放文件
        self.setAcceptDrops(True)
        self.create_widgets()
        self.setup_layout()
        self.set_window_properties()

    def create_widgets(self):
        self.line_count_field = QLineEdit()
        self.part_path_field = QLineEdit()

        # 创建一个按钮组
        self.buttonGroup = QButtonGroup()
        self.line_radio_button = QRadioButton("按行数分割")
        self.line_radio_button.setChecked(True)
        self.line_radio_button.toggled.connect(self.on_radio_button_toggled)
        self.size_radio_button = QRadioButton("按大小分割")
        self.size_radio_button.setChecked(False)
        self.size_radio_button.toggled.connect(self.on_radio_button_toggled)
        self.buttonGroup.addButton(self.size_radio_button)
        self.buttonGroup.addButton(self.line_radio_button)

        self.split_button = QPushButton('分割文件')
        self.split_button.clicked.connect(self.split_file)

        self.file_encoding_box = QComboBox(self)
        self.file_encoding_box.addItems(["utf-8", "gbk", "big5", "ascii", "iso-8859-1"])
        self.file_encoding_box.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.file_encoding_box.setEditable(True)

        self.file_list_widget = FileListWidget()
        self.file_list_widget.fileChanged.connect(self.ui_changed_trigger)

        self.drag_rect_widget = DragRectWidget()
        self.drag_rect_widget.file_dropped.connect(self.file_list_widget.add_files)

    def setup_layout(self):
        layout = QGridLayout()
        layout.addWidget(QLabel("请选择文件编码:"), 1, 0)
        layout.addWidget(self.file_encoding_box, 1, 1)
        layout.addWidget(self.line_radio_button, 2, 0)
        layout.addWidget(self.size_radio_button, 2, 1)
        layout.addWidget(QLabel('请输入欲分割行数/大小：'), 3, 0)
        layout.addWidget(self.line_count_field, 3, 1)
        layout.addWidget(QLabel('请输入欲保存的目录\n(留空默认当前目录下自动新建子目录)：'), 4, 0)
        layout.addWidget(self.part_path_field, 4, 1)
        layout.addWidget(self.drag_rect_widget, 5, 0, 1, 2)
        layout.addWidget(self.split_button, 6, 0, 1, 2)
        layout.addWidget(self.file_list_widget, 8, 0, 1, 2)
        layout.setColumnStretch(0, 4)
        layout.setColumnStretch(1, 6)
        self.setLayout(layout)

    def set_window_properties(self):
        pixmap = QPixmap()
        logo_data_bytes = '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'.encode()
        pixmap.loadFromData(base64.b64decode(logo_data_bytes), 'ico')
        self.setWindowIcon(QIcon(pixmap))
        self.setWindowTitle('奥怪文件分割v1.3')
        self.show()

    def ui_changed_trigger(self):
        """
        UI 变化时触发的信号处理函数。
        """
        self.split_file()

    def handle_events(self, file_signal_data: FileSignalData):
        """
        处理线程事件，更新进度条和显示分割完成信息。
        :param file_signal_data: 文件信号数据
        :type file_signal_data: FileSignalData
        """
        self.file_list_widget.set_progress(file_signal_data.file_path, file_signal_data.progress_value)
        if file_signal_data.progress_value >= 100:
            self._worker_dict.pop(file_signal_data.file_path, None)

    def split_file(self):
        """
        获取用户输入，创建 SplitFiles 线程对象，并启动分割文件的线程。
        如果输入不合法，显示相应警告信息。
        """
        line_count_text = self.line_count_field.text().strip()
        part_path = self.part_path_field.text()
        if part_path and not os.path.exists(part_path):
            QMessageBox.information(self, "警告", "请输入有效的保存目录")
            return

        fail_sf_count = 0
        file_encoding = self.file_encoding_box.currentText()
        for file_path in self.file_list_widget.get_file_paths_dic().keys():
            if file_path in self._worker_dict:
                continue
            sf = self.create_split_file_task(file_path, file_encoding, part_path, line_count_text)
            if sf:
                sf.start()
                sf.trigger.connect(self.handle_events)
                self._worker_dict[file_path] = sf
            else:
                fail_sf_count += 1

        if fail_sf_count > 0:
            QMessageBox.information(self, "警告", "请输入有效的分割行数或大小")

    def create_split_file_task(self, file_path, file_encoding, part_path, line_count_text):
        """
        根据用户选择的分割方式创建 SplitFiles 任务对象。
        :param file_path: 文件路径
        :param file_encoding: 文件编码
        :param part_path: 分割文件保存路径
        :param line_count_text: 分割行数/大小文本
        :return: SplitFiles 任务对象或 None（如果输入无效）
        """
        if self.size_radio_button.isChecked():
            max_file_size_kb = self.parse_file_size(line_count_text)
            if max_file_size_kb is None:
                return None
            return SplitFiles(self, file_path, file_encoding, part_path or '', None, max_file_size_kb)
        else:
            if not line_count_text.isdigit() or int(line_count_text) <= 0:
                return None
            return SplitFiles(self, file_path, file_encoding, part_path or '', int(line_count_text), None)

    def parse_file_size(self, size_text):
        """
        解析文件大小文本，支持带单位的大小（kb, mb, gb, tb）。
        :param size_text: 文件大小文本
        :return: 文件大小（以 kb 为单位）或 None（如果输入无效）
        """
        if size_text.isdigit():
            return int(size_text)
        unit_map = {'kb': 1, 'mb': 1024, 'gb': 1024 * 1024, 'tb': 1024 * 1024 * 1024}
        suffix = size_text[-2:].lower()
        size = size_text[:-2]
        if not size.isdigit() or suffix not in unit_map:
            return None
        return int(size) * unit_map[suffix]

    def dragEnterEvent(self, event):
        """
        重写拖放事件的处理方法，接受文本文件的拖放。
        :param event: 拖放事件
        :type event: QDragEnterEvent
        """
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """
        重写拖放事件的处理方法，获取拖放的文本文件路径，并显示在文件名字段中。
        如果文件类型不是文本文件，显示相应警告信息。
        :param event: 拖放事件
        :type event: QDropEvent
        """
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            file_paths = [url.toLocalFile() for url in mime_data.urls()]
            self.file_list_widget.add_files(file_paths)

    def on_radio_button_toggled(self):
        """
        按行数分割和按大小分割的单选按钮切换事件处理函数。
        """
        sender = self.sender()
        if isinstance(sender, QRadioButton):
            if sender.text() == "按行数分割" and sender.isChecked():
                self.line_count_field.setPlaceholderText('1')
            else:
                self.line_count_field.setPlaceholderText('1/1kb/1mb/1gb/1tb')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SplitFileGUI()
    sys.exit(app.exec_())
