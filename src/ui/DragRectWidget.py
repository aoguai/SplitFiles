from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QWidget, QFileDialog


class DragRectWidget(QWidget):
    file_dropped = pyqtSignal(list)

    def __init__(self):
        """
        拖拽文件的区域
        """
        super().__init__()
        self.setMinimumSize(150, 100)
        self.setMouseTracking(True)  # 启用鼠标跟踪
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # 设置焦点策略为强焦点

    def paintEvent(self, event):
        painter = QPainter(self)

        # 设置虚线边框
        pen = QPen()
        pen.setColor(QColor(156, 156, 156))  # 设置边框颜色为灰色
        pen.setStyle(Qt.PenStyle.DashLine)  # 设置为虚线样式
        pen.setWidth(2)
        painter.setPen(pen)

        # 绘制边框
        rect = self.rect()
        rect.adjust(1, 1, -1, -1)  # 调整矩形大小，以便虚线不被裁剪
        painter.drawRect(rect)

        # 居中显示文本
        text = "拖拽文件到此处\n或者从你的电脑中选择"
        text_rect = painter.boundingRect(rect, Qt.AlignmentFlag.AlignCenter, text)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, text)

    def mousePressEvent(self, event):
        self.select_files()
        super().mousePressEvent(event)

    def enterEvent(self, event):
        self.setCursor(Qt.CursorShape.PointingHandCursor)  # 鼠标移到上面时设置为手型样式

    def leaveEvent(self, event):
        self.unsetCursor()  # 鼠标离开时恢复默认样式

    def select_files(self):
        file_dialog = QFileDialog(self)
        file_paths, _ = file_dialog.getOpenFileNames(self, "选择文件", "", "可分割文件 (*.txt; *.csv; *.jsonl)")

        if file_paths:
            # 发射信号，将文件路径列表传递给连接的槽
            self.file_dropped.emit(file_paths)
