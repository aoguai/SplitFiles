import sys
import base64
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QProgressBar, \
    QMessageBox
from SplitFiles import SplitFiles


class SplitFileGUI(QWidget):
    def __init__(self):
        super().__init__()
        # 支持拖放文件
        self.setAcceptDrops(True)
        # 调用Drops方法
        # Create progress bar
        self.progress_bar = QProgressBar(self)

        # Create input fields
        self.file_name_field = QLineEdit()
        self.line_count_field = QLineEdit('10000')
        self.part_path_field = QLineEdit()

        # Create text prompts
        file_name_prompt = QLabel('请输入欲分割的文本文件路径：')
        line_count_prompt = QLabel('请输入欲分割行数：')
        part_path_prompt = QLabel('请输入欲保存的目录(留空默认当前目录下自动新建子目录)：')

        # Create button
        split_button = QPushButton('分割文件')
        split_button.clicked.connect(self.split_file)

        # Create layout
        layout = QGridLayout()
        layout.addWidget(file_name_prompt, 0, 0)
        layout.addWidget(self.file_name_field, 0, 1)
        layout.addWidget(line_count_prompt, 1, 0)
        layout.addWidget(self.line_count_field, 1, 1)
        layout.addWidget(part_path_prompt, 2, 0)
        layout.addWidget(self.part_path_field, 2, 1)
        layout.addWidget(split_button, 3, 0, 1, 2)
        layout.addWidget(self.progress_bar, 5, 0, 1, 2)
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('奥怪文本分割v1.1')

        pixmap = QPixmap()
        logo_data_bytes = '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'.encode()
        pixmap.loadFromData(base64.b64decode(logo_data_bytes), 'ico')
        self.setWindowIcon(QIcon(pixmap))
        self.show()

    def handle_events(self, code, data = None):
        if (code == 0):
            self.progress_bar.setRange(1, data)  # Set range of progress bar
            return
        
        if (code == 1):
            self.progress_bar.setValue(self.progress_bar.value() + 1)  # Update progress bar value
            return

        if (code == -1): 
            self.progress_bar.reset()  # Reset progress bar
            QMessageBox.information(self, "已完成", "文件分割已完成！")
            return

    def split_file(self):
        file_name = self.file_name_field.text()
        if len(self.line_count_field.text().strip()) > 0:
            line_count = int(self.line_count_field.text())
            if line_count <= 0:
                QMessageBox.information(self, "警告", "分割行数不得小于等于0")
                self.line_count_field.clear()
                return
        else:
            QMessageBox.information(self, "警告", "分割行数不得小于等于0")
            self.line_count_field.clear()
            return
        part_path = self.part_path_field.text()

        self.sf = SplitFiles(self, file_name, line_count, part_path)
        self.sf.start()
        # 线程自定义信号连接的槽函数
        self.sf.trigger.connect(self.handle_events)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # Get the file path from the dropped file
        file_path = event.mimeData().urls()[0].toLocalFile()
        if file_path[-4:] == '.txt' or file_path[-4:] == '.csv':
            # Set the file name field to the file path
            self.file_name_field.setText(file_path)
        else:
            QMessageBox.information(self, "警告", "只支持文本文件")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = SplitFileGUI()
    sys.exit(app.exec_())
