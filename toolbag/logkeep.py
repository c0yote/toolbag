import argparse
import os.path
import shutil

class Log:
  BYTES_IN_MEGABYTE = 1000000
  DEFAULT_CLONE_EXTENSION = '.prev'
  
  def __init__(self, file_path):
    Log._raise_if_not_a_file(file_path)
    
    self._size = os.path.getsize(file_path)
    self._line_count = Log._count_lines_in_file(file_path)
    self._file_path = file_path
    
  def get_file_size_in_bytes(self):
    return self._size
    
  def get_file_size_in_megabytes(self):
    return float(self._size / Log.BYTES_IN_MEGABYTE)
  
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

  @staticmethod
  def _raise_if_not_a_file(file_path):
    if not os.path.isfile(file_path):
      raise FileNotFoundError(f'No file found at \'{file_path}\'.')
    
class _Application:
  DESCRIPTION = ('Checks user defined thresholds (such as size or line count) '
                 'to decide when to create backups and clear out logs.\n\n'
                 'The application will check the defined theshold, copy the '
                 'existing log to a backup, and then clear out the primary '
                 'log.  Existing backups will be overwritten with the latest.')
                 
  def __init__(self):
    arg_parser = _Application._build_arg_parser()
    args = arg_parser.parse_args()
    
    self._line_limit = args.line_limit
    self._size_limit_mb = args.size_limit
    self._work_log = Log(args.log_file)

  def run(self):
    if self._is_past_line_threshold() or self._is_past_size_threshold():
      self._work_log.clone_to_a_backup()
      self._work_log.clear_original_file()

  def _is_past_line_threshold(self):
    if self._line_limit is not None:
      return self._work_log.get_line_count() > self._line_limit
    else:
      return False
  
  def _is_past_size_threshold(self):  
    if self._size_limit_mb is not None:
      return self._work_log.get_file_size_in_megabytes() > self._size_limit_mb
    else:
      return False

  @staticmethod
  def _build_arg_parser():
    ARG_FILE_HELP = 'The target log file.'
    ARG_LINE_HELP = 'The maximum number of lines the log may have before backup.'
    ARG_SIZE_HELP = 'The maximum size (MB) the log may be before backup.'
    
    parser = argparse.ArgumentParser(description=_Application.DESCRIPTION)
    parser.add_argument('--size_limit', help=ARG_LINE_HELP, type=int)
    parser.add_argument('--line_limit', help=ARG_SIZE_HELP, type=int)
    parser.add_argument('log_file', help=ARG_FILE_HELP)
    return parser
      
    
if __name__ == '__main__':
  app = _Application()
  app.run()  
  