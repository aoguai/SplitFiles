import os
import typing
from typing import List
from PyQt5.QtCore import QThread, pyqtSignal
from model.FileSignalData import FileSignalData


class SplitFiles(QThread):
    trigger = pyqtSignal(FileSignalData)
    """分割文件"""

    def __init__(self, self_windows, file_name: str, file_encoding='utf-8', part_path='',
                 line_count: typing.Optional[int] = None,
                 max_file_size_kb: typing.Optional[int] = None):
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
        :type max_file_size_kb: int or None
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
        if not self.validate_file():
            return
        self.total_lines = self.count_lines()
        self.trigger.emit(FileSignalData(self.file_name, self.total_lines, 0))

        if self.max_file_size_kb:
            self.split_file(self.split_file_by_size)
        else:
            self.split_file(self.split_file_by_lines)

    def validate_file(self) -> bool:
        if not self.file_name or not os.path.exists(self.file_name):
            print(f"{self.file_name} 不是有效的文件")
            return False
        return True

    def count_lines(self) -> int:
        try:
            with open(self.file_name, encoding=self.file_encoding) as f:
                return sum(1 for _ in f)
        except IOError as err:
            print(err)
            return 0

    def split_file(self, split_method):
        try:
            with open(self.file_name, encoding=self.file_encoding) as f:
                temp_count, temp_content = self.init_temp_vars()
                part_num = 1
                for line_num, line in enumerate(f, start=1):
                    self.current_lines = line_num
                    temp_count, temp_content, part_num = split_method(line, temp_count, temp_content, part_num)
                    self.update_progress()
                if temp_content:
                    self.write_file(part_num, temp_count, temp_content)
        except IOError as err:
            print(err)

    def split_file_by_lines(self, line, temp_count, temp_content, part_num):
        temp_content.append(line)
        temp_count += 1
        if temp_count == self.line_count:
            self.write_file(part_num, temp_count, temp_content)
            part_num += 1
            temp_count, temp_content = self.init_temp_vars()
        return temp_count, temp_content, part_num

    def split_file_by_size(self, line, temp_count, temp_content, part_num):
        line_size = len(line.encode(self.file_encoding))
        if sum(len(l.encode(self.file_encoding)) for l in temp_content) + line_size < self.max_file_size_kb * 1024:
            temp_content.append(line)
            temp_count += 1
        else:
            self.write_file(part_num, temp_count, temp_content)
            part_num += 1
            temp_count, temp_content = 1, [line]
        return temp_count, temp_content, part_num

    def init_temp_vars(self):
        return 0, []

    def update_progress(self):
        current_percent = int((self.current_lines / self.total_lines) * 100)
        if self.current_precent != current_percent:
            self.current_precent = current_percent
            self.trigger.emit(FileSignalData(self.file_name, self.total_lines, self.current_precent))

    def get_part_file_name(self, part_num: int, temp_count: int) -> str:
        temp_name, file_extension = os.path.splitext(os.path.basename(self.file_name))
        temp_path = self.part_path or os.path.join(os.path.dirname(self.file_name), temp_name)
        os.makedirs(temp_path, exist_ok=True)
        return f"{temp_path}{os.sep}{temp_name}_part{part_num}_{temp_count}{file_extension}"

    def write_file(self, part_num: int, temp_count: int, line_content: List[str]):
        part_file_name = self.get_part_file_name(part_num, temp_count)
        try:
            with open(part_file_name, "w", encoding=self.file_encoding) as part_file:
                part_file.writelines(line_content)
        except IOError as err:
            print(err)
