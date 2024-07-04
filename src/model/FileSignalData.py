class FileSignalData:

    def __init__(self, file_path: str = '', total_lines: int = 0, progress_value: int = 0):
        """
        文件信号数据

        :param file_path: 文件路径
        :type file_path: str
        :param total_lines: 总行数
        :type total_lines: int
        :param progress_value: 进度值
        :type progress_value: int
        """

        super().__init__()

        self.file_path = file_path
        self.total_lines = total_lines
        self.progress_value = progress_value
