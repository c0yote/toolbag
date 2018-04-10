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

  def clear_original_file(self):
    Log._clear_file_contents(self._file_path)
    
  def clone_to_a_backup(self, user_defined_path=None):
    if user_defined_path:
      shutil.copy2(self._file_path, user_defined_path)
    else:
      shutil.copy2(self._file_path, self._file_path + Log.DEFAULT_CLONE_EXTENSION)

  def get_file_path(self):
    return self._file_path
      
  @staticmethod
  def _count_lines_in_file(file_path):
    line_count = 0
  
    with open(file_path, 'r') as log_file:
      for line in log_file:
        line_count += 1
        
    return line_count

  @staticmethod
  def _clear_file_contents(file_path):
    if os.path.isfile(file_path):
      open(file_path, 'w').close()
    else:
      raise FileNotFoundError(f'No file found at \'{file_path}\'.')
    
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
    
    try:
      self._work_log = Log(args.log_file)
    except PermissionError as e:
      raise RuntimeError(f'Insufficient permissions to access file: {args.log_file}')
    except FileNotFoundError as e:
      raise RuntimeError(f'Could not locate a file at: {args.log_file}')

  def run(self):
    try:
      if self._is_past_line_threshold() or self._is_past_size_threshold():
        self._work_log.clone_to_a_backup()
        self._work_log.clear_original_file()
    except PermissionError as e:
      raise RuntimeError(f'Insufficient permissions to access file: {self._work_log.get_file_path()}')
    except FileNotFoundError as e:
      raise RuntimeError(f'Could not locate a file at: {self._work_log.get_file_path()}')

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
    parser.add_argument('--size_limit', help=ARG_LINE_HELP, type=float)
    parser.add_argument('--line_limit', help=ARG_SIZE_HELP, type=int)
    parser.add_argument('log_file', help=ARG_FILE_HELP)
    return parser

def main():
  try:
    app = _Application()
    app.run()
  except RuntimeError as e:
    print('Error: '+str(e))
  except Exception as e:
    print('Unhandled Exception: '+repr(e))

if __name__ == '__main__':
  main()
