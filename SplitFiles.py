import os
import chardet
from PyQt5.QtCore import QThread, pyqtSignal


def detect_file_encoding(file_path):
    with open(file_path, 'rb') as file:
        # 读取文件前 1024 字节，用于判断文件编码
        return chardet.detect(file.read(1024))['encoding']


class SplitFiles(QThread):
    trigger = pyqtSignal(int, object)
    """按行分割文件"""

    def __init__(self, self_windows, file_name, line_count=200, part_path=''):
        """
        初始化分割文件的线程对象

        :param self_windows: 调用该线程的主窗口对象
        :type self_windows: object
        :param file_name: 要分割的源文件名
        :type file_name: str
        :param line_count: 分割后的文件行数，默认为 200
        :type line_count: int
        :param part_path: 存放分割文件的目录，默认为空，表示在源文件相同目录下建立临时文件夹
        :type part_path: str
        """

        super(SplitFiles, self).__init__()
        self.file_name = file_name
        self.line_count = line_count
        self.part_path = part_path
        self.windows = self_windows
        self.total_lines = 0

    def run(self):
        """
        重写 QThread 的 run 方法，在线程启动时执行分割文件的操作
        """

        self.split_file()

    def split_file(self):
        """
        分割文件的核心逻辑

        1. 获取总行数
        2. 发送信号通知主窗口总行数
        3. 逐行读取源文件，按设定行数分割并写入新文件
        4. 发送信号通知主窗口分割进度
        """

        if not self.file_name or not os.path.exists(self.file_name):
            print("%s 不是有效的文件" % self.file_name)
            return

        try:
            with open(self.file_name, encoding=detect_file_encoding(self.file_name)) as f:
                self.total_lines = sum(1 for _ in f)

            self.trigger.emit(0, self.total_lines)

            with open(self.file_name, encoding=detect_file_encoding(self.file_name)) as f:
                temp_count = 0
                temp_content = []
                part_num = 1

                for line_count, line in enumerate(f, start=1):
                    if temp_count < self.line_count:
                        temp_count += 1
                    else:
                        self.write_file(part_num, temp_count, temp_content)
                        part_num += 1
                        temp_count = 1
                        temp_content = []

                    temp_content.append(line)
                    self.trigger.emit(1, None)

                else:
                    self.write_file(part_num, temp_count, temp_content)

        except IOError as err:
            print(err)

    def get_part_file_name(self, part_num, temp_count):
        """
        获取分割后的文件名称

        如果未指定目录，则在源文件相同目录下建立临时文件夹 temp_part_file，
        然后将分割后的文件放到该路径下。

        :param part_num: 分割文件的编号
        :type part_num: int
        :param temp_count: 临时计数，用于文件名
        :type temp_count: int
        :return: 分割后的文件名
        :rtype: str
        """

        temp_name, file_extension = os.path.splitext(os.path.basename(self.file_name))
        if self.part_path == '':
            temp_path = os.path.join(os.path.dirname(self.file_name), temp_name)
        else:
            temp_path = self.part_path

        if not os.path.exists(temp_path):
            os.makedirs(temp_path)

        part_file_name = f"{temp_path}{os.sep}{temp_name}_part{part_num}_{temp_count}{file_extension}"
        return part_file_name

    def write_file(self, part_num, temp_count, line_content):
        """
        将按行分割后的内容写入相应的分割文件中

        :param part_num: 分割文件的编号
        :type part_num: int
        :param temp_count: 临时计数，用于文件名
        :type temp_count: int
        :param line_content: 分割后的内容
        :type line_content: list
        """

        part_file_name = self.get_part_file_name(part_num, temp_count)

        try:
            with open(part_file_name, "w", encoding=detect_file_encoding(self.file_name)) as part_file:
                part_file.writelines(line_content)

        except IOError as err:
            print(err)
