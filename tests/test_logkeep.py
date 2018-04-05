import os
import unittest
from unittest import skip
from unittest.mock import MagicMock, mock_open, patch

def fix_iteration_in_mock_open(open_mock):
  """ A test utility function to help with file open mocking.
  """
  open_mock.return_value.__iter__ = lambda self : iter(self.readline, '')
  
from toolbag.logkeep import _Application, Log

BYTES_IN_MEGABYTE = 1000000
TEST_LOG_PATH = '/some/path/to/log.log'
TEST_LOG_DATA = f'line 0{os.linesep}line 1{os.linesep} line 2'
TEST_LOG_DATA_SIZE = len(TEST_LOG_DATA.encode('utf-8'))
TEST_LOG_DATA_LINE_CNT = 3
TEST_USER_DEFINED_CLONE_PATH = '/user/path/to/log.bak'
TEST_LIMIT_VALUE_A = 10
TEST_LIMIT_VALUE_B = 11
TEST_LIMIT_GREATER = 12
TEST_ARGS = ['app', TEST_LOG_PATH]
TEST_SIZE_ARGS = ['app', '--size_limit', f'{TEST_LIMIT_VALUE_A}', TEST_LOG_PATH]
TEST_LINE_ARGS = ['app', '--line_limit', f'{TEST_LIMIT_VALUE_B}', TEST_LOG_PATH]
TEST_SIZE_AND_LINE_ARGS = ['app', '--size_limit', f'{TEST_LIMIT_VALUE_A}', 
                            '--line_limit', f'{TEST_LIMIT_VALUE_B}',
                            TEST_LOG_PATH]
                            
class Log_TestCase(unittest.TestCase):
  """ When we don't care about the mocks generated during patching, '*args' is 
      used in the test function parameters so there isn't a long list of useless 
      patch parameters taking up space.
  """

  def test_constructor_excepts_on_no_file(self):
    with self.assertRaises(FileNotFoundError):
      log = Log(TEST_LOG_PATH)

  def test_constructor_excepts_when_path_is_not_a_file(self, *args):
    with self.assertRaises(FileNotFoundError):
      log = Log('./')
  
  @patch('os.path.getsize', return_value=TEST_LOG_DATA_SIZE)
  @patch('toolbag.logkeep.Log._raise_if_not_a_file')
  @patch('builtins.open', new_callable=mock_open, read_data=TEST_LOG_DATA)
  def test_constructor_computes_size(self, *args):
    log = Log(TEST_LOG_PATH)
    self.assertEqual(TEST_LOG_DATA_SIZE, log.get_file_size_in_bytes())
    self.assertEqual(TEST_LOG_DATA_SIZE/BYTES_IN_MEGABYTE, log.get_file_size_in_megabytes())
    
  @patch('os.path.getsize', return_value=TEST_LOG_DATA_SIZE)
  @patch('toolbag.logkeep.Log._raise_if_not_a_file')
  @patch('builtins.open', new_callable=mock_open, read_data=TEST_LOG_DATA)
  def test_constructor_counts_lines(self, open_, *args):
    fix_iteration_in_mock_open(open_)
    log = Log(TEST_LOG_PATH)
    self.assertEqual(TEST_LOG_DATA_LINE_CNT, log.get_line_count())

  @patch('builtins.open', new_callable=mock_open, read_data=TEST_LOG_DATA)
  def test__count_lines_in_file(self, open_):
    fix_iteration_in_mock_open(open_)
  
    line_count = Log._count_lines_in_file(TEST_LOG_PATH)
    open_.assert_called_with(TEST_LOG_PATH, 'r')
    self.assertEqual(line_count, TEST_LOG_DATA_LINE_CNT)
    
  @patch('os.path.getsize', return_value=TEST_LOG_DATA_SIZE)
  @patch('builtins.open', new_callable=mock_open, read_data=TEST_LOG_DATA)
  @patch('toolbag.logkeep.Log._raise_if_not_a_file')
  @patch('shutil.copy2')
  def test_clone_to_a_backup_default(self, copy2_mock, *args):
    log = Log(TEST_LOG_PATH)
    log.clone_to_a_backup()
    copy2_mock.assert_called_with(TEST_LOG_PATH, TEST_LOG_PATH+'.prev')

  @patch('os.path.getsize', return_value=TEST_LOG_DATA_SIZE)
  @patch('builtins.open', new_callable=mock_open, read_data=TEST_LOG_DATA)
  @patch('toolbag.logkeep.Log._raise_if_not_a_file')
  @patch('shutil.copy2')
  def test_clone_to_a_backup_with_user_defined_path(self, copy2_mock, *args):
    log = Log(TEST_LOG_PATH)
    log.clone_to_a_backup(TEST_USER_DEFINED_CLONE_PATH)
    copy2_mock.assert_called_with(TEST_LOG_PATH, TEST_USER_DEFINED_CLONE_PATH)
    
    
    
class Application_TestCase(unittest.TestCase):
  @patch('sys.argv', TEST_SIZE_ARGS)
  @patch('toolbag.logkeep.Log')
  def test_size_threshold_storage(self, *args):
    app = _Application()
    self.assertEqual(app._size_limit_mb, TEST_LIMIT_VALUE_A)
    self.assertEqual(app._line_limit, None)
    
  @patch('sys.argv', TEST_LINE_ARGS)
  @patch('toolbag.logkeep.Log')
  def test_line_threshold_storage(self, *args):
    app = _Application()
    self.assertEqual(app._size_limit_mb, None)
    self.assertEqual(app._line_limit, TEST_LIMIT_VALUE_B)
  
  @patch('sys.argv', TEST_SIZE_AND_LINE_ARGS)
  @patch('toolbag.logkeep.Log')
  def test_size_and_line_threshold_storage(self, *args):
    app = _Application()
    self.assertEqual(app._size_limit_mb, TEST_LIMIT_VALUE_A)
    self.assertEqual(app._line_limit, TEST_LIMIT_VALUE_B)
    
  @patch('sys.argv', TEST_ARGS)
  @patch('toolbag.logkeep.Log')
  def test_no_threshold_storage(self, *args):
    app = _Application()
    self.assertEqual(app._size_limit_mb, None)
    self.assertEqual(app._line_limit, None)

  @patch('sys.argv', TEST_ARGS)
  @patch('toolbag.logkeep.Log')  
  def test_work_log_creation(self, log_mock):
    app = _Application()
    log_mock.assert_called_with(TEST_LOG_PATH)

  @patch('sys.argv', TEST_ARGS)
  @patch('toolbag.logkeep.Log')  
  def test_work_log_storage(self, log_mock):
    app = _Application()
    handle = log_mock()
    self.assertEqual(app._work_log, handle)

  @patch('sys.argv', TEST_ARGS)
  @patch('toolbag.logkeep.Log')
  def test_does_not_clone_log_on_no_thresholds(self, log_mock):
    app = _Application()
    app.run()
    
    log_mock.clone_to_a_backup.assert_not_called()

  @patch('sys.argv', TEST_SIZE_ARGS)
  @patch('toolbag.logkeep.Log')
  def test_clones_log_on_size_threshold(self, log_mock):
    handle = log_mock()
    handle.get_file_size_in_megabytes.return_value = TEST_LIMIT_GREATER
  
    app = _Application()
    app.run()
    
    handle.clone_to_a_backup.assert_called_with()
    
  @patch('sys.argv', TEST_LINE_ARGS)
  @patch('toolbag.logkeep.Log')
  def test_clones_log_on_line_count_threshold(self, log_mock):
    handle = log_mock()
    handle.get_line_count.return_value = TEST_LIMIT_GREATER
  
    app = _Application()
    app.run()
    
    handle.clone_to_a_backup.assert_called_with()
    
  @patch('sys.argv', TEST_SIZE_AND_LINE_ARGS)
  @patch('toolbag.logkeep.Log')
  def test_clones_log_on_sizeand_line_count_threshold(self, log_mock):
    handle = log_mock()
    handle.get_line_count.return_value = TEST_LIMIT_GREATER
  
    app = _Application()
    app.run()
    
    handle.clone_to_a_backup.assert_called_with()

  #def test_error_on_no_permissions(self):
    #pass