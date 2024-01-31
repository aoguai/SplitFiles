import os
import typing
from PyQt5.QtCore import QThread, pyqtSignal
from model.FileSignalData import FileSignalData

class SplitFiles(QThread):
    trigger = pyqtSignal(FileSignalData)
    """按行分割文件"""

    def __init__(self, self_windows, file_name: str, file_encoding='utf-8', part_path='', line_count: typing.Optional[int]=None,
                 max_file_size_kb: typing.Optional[int]=None):
        """
        初始化分割文件的线程对象

        :param self_windows: 调用该线程的主窗口对象
        :type self_windows: object
        :param file_name: 要分割的源文件名
        :type file_name: str
        :param file_encoding: 文件编码
        :type file_encoding: str
        :param part_path: 存放分割文件的目录，默认为空，表示在源文件相同目录下建立临时文件夹
        :type part_path: str
        :param line_count: 分割后的文件行数
        :type line_count: int or None
        :param max_file_size_kb: 分割后的文件大小，单位kb
        :type line_count: int or None
        """

        super(SplitFiles, self).__init__()
        self.file_name = file_name
        self.file_encoding = file_encoding
        self.line_count = line_count
        self.part_path = part_path
        self.windows = self_windows
        self.total_lines = 0
        self.current_lines = 1
        self.current_precent = 0
        self.max_file_size_kb = max_file_size_kb

    def run(self):
        """
        重写 QThread 的 run 方法，在线程启动时执行分割文件的操作
        """
        if self.max_file_size_kb:
            self.split_file_by_size()
        else:
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
        if not self.line_count:
            return

        try:
            with open(self.file_name, encoding=self.file_encoding) as f:
                self.total_lines = sum(1 for _ in f)
                self.trigger.emit(FileSignalData(self.file_name, self.total_lines, 0))

            with open(self.file_name, encoding=self.file_encoding) as f:
                temp_count = 0
                temp_content = []
                part_num = 1

                for line_num, line in enumerate(f, start=1):
                    self.current_lines = line_num
                    temp_content.append(line)
                    temp_count += 1

                    if temp_count == self.line_count:
                        self.write_file(part_num, temp_count, temp_content)
                        part_num += 1
                        temp_count = 0
                        temp_content = []

                    # 当进度百分比变化时才发送信号1更改状态
                    current_percent = int((self.current_lines / self.total_lines) * 100)
                    if self.current_precent != current_percent:
                        self.current_precent = current_percent
                        self.trigger.emit(FileSignalData(self.file_name, self.total_lines, self.current_precent))

                if temp_content:
                    self.write_file(part_num, temp_count, temp_content)
        except IOError as err:
            print(err)

    def get_part_file_name(self, part_num: int, temp_count: int):
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

    def write_file(self, part_num: int, temp_count: int, line_content: list[str]):
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
            with open(part_file_name, "w", encoding=self.file_encoding) as part_file:
                part_file.writelines(line_content)

        except IOError as err:
            print(err)

    # 新增分支业务处理文件大小切割
    def split_file_by_size(self):
        if not self.file_name or not os.path.exists(self.file_name):
            print("%s 不是有效的文件" % self.file_name)
            return
        if not self.max_file_size_kb:
            return

        try:
            with open(self.file_name, encoding=self.file_encoding) as f:
                self.total_lines = sum(1 for _ in f)
                self.trigger.emit(FileSignalData(self.file_name, self.total_lines, 0))

            with open(self.file_name, encoding=self.file_encoding) as f:
                temp_count = 0
                temp_content = []
                part_num = 1
                current_file_size = 0

                for line_num, line in enumerate(f, start=1):
                    self.current_lines = line_num
                    line_size = len(line.encode(self.file_encoding))
                    if current_file_size + line_size < self.max_file_size_kb * 1024:
                        temp_count += 1
                        current_file_size += line_size
                        temp_content.append(line)
                    else:
                        # print(str(current_file_size / 1024) + 'kb')
                        self.write_file(part_num, temp_count, temp_content)
                        part_num += 1
                        temp_count = 1
                        temp_content = [line]
                        current_file_size = line_size

                    # 当进度百分比变化时才发送信号1更改状态
                    current_percent = int((self.current_lines / self.total_lines) * 100)
                    if self.current_precent != current_percent:
                        self.current_precent = current_percent
                        self.trigger.emit(FileSignalData(self.file_name, self.total_lines, self.current_precent))

                else:
                    self.write_file(part_num, temp_count, temp_content)
        except IOError as err:
            print(err)
