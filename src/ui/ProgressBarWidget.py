from PyQt5.QtWidgets import QWidget, QProgressBar, QVBoxLayout


class ProgressBarWidget(QWidget):
    def __init__(self):
        """
        进度条组件
        """

        super().__init__()

        # 创建进度条
        self.progress_bar = QProgressBar(self)

        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        # 设置初始属性
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

    def set_progress(self, value: int):
        """
        设置进度条的值并更新标签。

        :param value: 进度值
        :type value: int
        """

        if value < 0:
            value = 0
        elif value > 100:
            value = 100

        self.progress_bar.setValue(value)

    def get_progress(self):
        """
        获取进度条的值。

        :return: 进度条的值
        :rtype: int
        """

        return self.progress_bar.value()

    def reset(self):
        self.progress_bar.reset()
