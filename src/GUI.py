import base64
import os
import sys
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox, \
    QFileDialog, QRadioButton, QButtonGroup, QComboBox
from ProgressBarUI import ProgressBarUI
from SplitFiles import SplitFiles


class SplitFileGUI(QWidget):
    def __init__(self):
        """
        初始化 GUI 界面

        包括拖放文件支持、进度条、输入字段、文本提示、按钮、布局和窗口属性的设置。
        """

        super().__init__()
        # 支持拖放文件
        self.setAcceptDrops(True)
        # 调用Drops方法
        # Create progress bar
        self.progress_bar_ui = ProgressBarUI()

        # 创建输入字段
        self.file_name_field = QLineEdit()
        # 为输入框添加双击事件
        self.file_name_field.setReadOnly(True)
        self.file_name_field.setMouseTracking(True)
        self.file_name_field.installEventFilter(self)
        self.line_count_field = QLineEdit()
        self.line_count_field.setPlaceholderText('1')
        self.part_path_field = QLineEdit()

        # 创建一个按钮组
        self.buttonGroup = QButtonGroup()

        self.line_radio_button = QRadioButton("按行数分割")
        self.line_radio_button.setChecked(True)  # 默认按行数分割
        self.line_radio_button.toggled.connect(self.on_radio_button_toggled)
        self.size_radio_button = QRadioButton("按大小分割")
        self.size_radio_button.setChecked(False)
        self.size_radio_button.toggled.connect(self.on_radio_button_toggled)

        self.buttonGroup.addButton(self.size_radio_button)
        self.buttonGroup.addButton(self.line_radio_button)

        # 创建文本提示
        file_name_prompt = QLabel('请输入欲分割的文件路径：')
        line_count_prompt = QLabel('请输入欲分割行数/大小(不含单位默认kb)：')
        part_path_prompt = QLabel('请输入欲保存的目录(留空默认当前目录下自动新建子目录)：')

        # Create button
        self.split_button = QPushButton('分割文件')
        self.split_button.clicked.connect(self.split_file)

        file_encoding_prompt = QLabel("请选择文件编码:")
        self.file_encoding_box = QComboBox(self)
        self.file_encoding_box.addItems(["utf-8", "gbk", "big5", "ascii", "iso-8859-1"])
        self.file_encoding_box.setInsertPolicy(QComboBox.NoInsert)
        self.file_encoding_box.setEditable(True)  # 设置为不可编辑，确保只能选择列表中的选项

        # 创建布局
        layout = QGridLayout()
        layout.addWidget(file_name_prompt, 0, 0)
        layout.addWidget(self.file_name_field, 0, 1)
        layout.addWidget(file_encoding_prompt, 1, 0)
        layout.addWidget(self.file_encoding_box, 1, 1)
        layout.addWidget(self.line_radio_button, 2, 0)
        layout.addWidget(self.size_radio_button, 2, 1)
        layout.addWidget(line_count_prompt, 3, 0)
        layout.addWidget(self.line_count_field, 3, 1)
        layout.addWidget(part_path_prompt, 4, 0)
        layout.addWidget(self.part_path_field, 4, 1)
        layout.addWidget(self.split_button, 5, 0, 1, 2)
        layout.addWidget(self.progress_bar_ui, 6, 0, 1, 2)
        self.setLayout(layout)

        # 设置窗口图标
        pixmap = QPixmap()
        logo_data_bytes = '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'.encode()
        pixmap.loadFromData(base64.b64decode(logo_data_bytes), 'ico')
        self.setWindowIcon(QIcon(pixmap))

        # 设置窗口属性
        self.setWindowTitle('奥怪文件分割v1.2')
        self.show()

    def handle_events(self, code, data=None):
        """
        处理线程事件，更新进度条和显示分割完成信息。

        :param code: 事件代码，0表示更新总量，1表示更新进度条值
        :type code: int
        :param data: 事件数据，用于设置进度条范围的最大值
        :type data: int or None
        """

        # print("接收到信号 %s, 承载数据为 %s" % (code, data))
        if code == 0:
            return

        if code == 1:
            self.progress_bar_ui.set_progress(data)  # Update progress bar value

            if data == 100:
                QMessageBox.information(self, "已完成", "文件分割已完成！")
                self.split_button.setEnabled(True)
            return

    def split_file(self):
        """
        获取用户输入，创建 SplitFiles 线程对象，并启动分割文件的线程。

        如果输入不合法，显示相应警告信息。
        """

        file_name = self.file_name_field.text()
        line_count_text = self.line_count_field.text().strip()
        part_path = self.part_path_field.text()

        if not file_name or not os.path.exists(file_name):
            QMessageBox.information(self, "警告", f"{file_name} 不是有效的文件")
            return

        if part_path and not os.path.exists(part_path):
            QMessageBox.information(self, "警告", "请输入有效的保存目录")
            return

        file_encoding = self.file_encoding_box.currentText()

        # 判断分割方式
        if self.size_radio_button.isChecked():
            # 按大小分割
            if line_count_text.isdigit():
                max_file_size_kb = int(line_count_text)
            else:
                unit_map = {'kb': 1, 'mb': 1024, 'gb': 1024 * 1024, 'tb': 1024 * 1024 * 1024}
                suffix = line_count_text[-2:].lower()
                size = line_count_text[:-2]
                if not size.isdigit():
                    QMessageBox.information(self, "警告", "请输入有效的分割大小（大于0的整数或者带单位的数字）")
                    return
                multiplier = unit_map.get(suffix)
                if multiplier is None:
                    QMessageBox.information(self, "警告", "请输入有效的分割大小（大于0的整数或者带单位的数字）\n注意：单位只支持kb/mb/gb/tb")
                    return
                max_file_size_kb = int(size) * multiplier
            self.sf = SplitFiles(self, file_name, file_encoding, part_path or '', None, max_file_size_kb)
        else:
            # 按行数分割
            if not line_count_text.isdigit():
                QMessageBox.information(self, "警告", "请输入有效的分割行数（大于0的整数）")
                return
            line_count = int(line_count_text)
            if line_count <= 0:
                QMessageBox.information(self, "警告", "请输入大于0的行数")
                return
            self.sf = SplitFiles(self, file_name, file_encoding, part_path or '', line_count, None)

        self.sf.start()
        # 线程自定义信号连接的槽函数
        self.sf.trigger.connect(self.handle_events)
        # 重置滚动条
        self.progress_bar_ui.reset()
        self.split_button.setEnabled(False)

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

        file_path = event.mimeData().urls()[0].toLocalFile()
        if file_path.endswith(('.txt', '.csv', '.jsonl')):
            # 将文件名字段设置为文件路径
            self.file_name_field.setText(file_path)
        else:
            QMessageBox.information(self, "警告", "只支持可分割文件")

    def eventFilter(self, obj, event):
        if obj == self.file_name_field and event.type() == 2:  # 2表示鼠标双击事件
            self.select_file()
        return super().eventFilter(obj, event)

    def select_file(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "选择文件", "", "可分割文件 (*.txt; *.csv; *.jsonl)")
        if file_path:
            self.file_name_field.setText(file_path)

    def on_radio_button_toggled(self):
        sender = self.sender()
        if sender.text() == "按行数分割":
            if sender.isChecked():
                self.line_count_field.setPlaceholderText('1')
                return
        self.line_count_field.setPlaceholderText('1/1kb/1mb/1gb/1tb')
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = SplitFileGUI()
    sys.exit(app.exec_())
