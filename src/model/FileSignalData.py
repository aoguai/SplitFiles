class FileSignalData:

    def __init__(self, file_path: str = '', total_lines: int = 0, progress_value: int = 0):
        super().__init__()
        
        self.file_path = file_path
        self.total_lines = total_lines
        self.progress_value = progress_value