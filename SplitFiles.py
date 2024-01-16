import os
from PyQt5.QtWidgets import QMessageBox


class SplitFiles():
    """按行分割文件"""

    def __init__(self, self_windows, file_name, line_count=200, part_path=''):
        """初始化要分割的源文件名和分割后的文件行数"""
        self.file_name = file_name
        self.line_count = line_count
        self.part_path = part_path
        self.windows = self_windows
        self.total_lines = 0

    def split_file(self):
        if self.file_name and os.path.exists(self.file_name):
            try:
                # Get total number of lines
                with open(self.file_name, encoding='UTF-8') as f:
                    self.total_lines = sum(1 for _ in f)

                self.windows.progress_bar.setRange(1, self.total_lines)  # Set range of progress bar

                with open(self.file_name, encoding='UTF-8') as f:
                    temp_count = 0
                    temp_content = []
                    part_num = 1
                    for line in f:
                        if temp_count < self.line_count:
                            temp_count += 1
                        else:
                            self.write_file(part_num, temp_count, temp_content)
                            part_num += 1
                            temp_count = 1
                            temp_content = []
                        temp_content.append(line)
                        self.windows.progress_bar.setValue(
                            self.windows.progress_bar.value() + 1)  # Update progress bar value
                    else:
                        self.write_file(part_num, temp_count, temp_content)
            except IOError as err:
                print(err)
        else:
            print("%s is not a validate file" % self.file_name)

    def get_part_file_name(self, part_num, temp_count):
        """"获取分割后的文件名称：如果未指定目录，则在源文件相同目录下建立临时文件夹temp_part_file，然后将分割后的文件放到该路径下"""
        temp_path = os.path.dirname(self.file_name)  # 获取文件的路径（不含文件名）
        temp_name, file_extension = os.path.splitext(os.path.basename(self.file_name))
        if self.part_path == '':
            part_file_name = temp_path + os.sep + temp_name
        else:
            part_file_name = self.part_path
        if not os.path.exists(part_file_name):  # 如果临时目录不存在则创建
            os.makedirs(part_file_name)
        part_file_name += os.sep + temp_name + "_part" + str(part_num) + "_" + str(temp_count) + file_extension
        return part_file_name

    def write_file(self, part_num, temp_count, *line_content):
        """将按行分割后的内容写入相应的分割文件中"""
        part_file_name = self.get_part_file_name(part_num, temp_count)
        try:
            with open(part_file_name, "w", encoding='UTF-8') as part_file:
                part_file.writelines(line_content[0])
                if self.windows.progress_bar.value() >= self.total_lines:
                    self.windows.progress_bar.reset()  # Reset progress bar
                    QMessageBox.information(self.windows, "已完成", "文件分割已完成！")
        except IOError as err:
            print(err)
