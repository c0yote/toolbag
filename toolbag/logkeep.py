import os.path
import shutil

class Log:
  DEFAULT_CLONE_EXTENSION = '.prev'
  
  def __init__(self, file_path):
    self._size = os.path.getsize(file_path)
    self._line_count = Log._count_lines_in_file(file_path)
    self._file_path = file_path
    
  def get_file_size_in_bytes(self):
    return self._size
  
  def get_line_count(self):
    return self._line_count
  
  def clone_to_a_backup(self, user_defined_path=None):
    if user_defined_path:
      shutil.copy2(self._file_path, user_defined_path)
    else:
      shutil.copy2(self._file_path, self._file_path + Log.DEFAULT_CLONE_EXTENSION)

  @staticmethod
  def _count_lines_in_file(file_path):
    line_count = 0
  
    with open(file_path, 'r') as log_file:
      for line in log_file:
        line_count += 1
        
    return line_count
    