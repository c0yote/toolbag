import os
import unittest
from unittest import skip
from unittest.mock import MagicMock, mock_open, patch

def fix_iteration_in_mock_open(open_mock):
  """ A test utility function to help with file open mocking.
  """
  open_mock.return_value.__iter__ = lambda self : iter(self.readline, '')

from toolbag.logkeep import Log

BYTES_IN_MEGABYTE = 1000000
TEST_LOG_PATH = '/some/path/to/log.log'
TEST_LOG_DATA = f'line 0{os.linesep}line 1{os.linesep} line 2'
TEST_LOG_DATA_SIZE = len(TEST_LOG_DATA.encode('utf-8'))
TEST_LOG_DATA_LINE_CNT = 3
TEST_USER_DEFINED_CLONE_PATH = '/user/path/to/log.bak'

class Log_TestCase(unittest.TestCase):
  def test_constructor_excepts_on_no_file(self):
    with self.assertRaises(FileNotFoundError):
      log = Log(TEST_LOG_PATH)

  def test_constructor_excepts_when_path_is_not_a_file(self, *stubs):
    with self.assertRaises(FileNotFoundError):
      log = Log('./')
  
  @patch('os.path.getsize', return_value=TEST_LOG_DATA_SIZE)
  @patch('toolbag.logkeep.Log._raise_if_not_a_file')
  @patch('builtins.open', new_callable=mock_open, read_data=TEST_LOG_DATA)
  def test_constructor_computes_size(self, *stubs):
    log = Log(TEST_LOG_PATH)
    self.assertEqual(TEST_LOG_DATA_SIZE, log.get_file_size_in_bytes())
    self.assertEqual(TEST_LOG_DATA_SIZE/BYTES_IN_MEGABYTE, log.get_file_size_in_megabytes())
    
  @patch('os.path.getsize', return_value=TEST_LOG_DATA_SIZE)
  @patch('toolbag.logkeep.Log._raise_if_not_a_file')
  @patch('builtins.open', new_callable=mock_open, read_data=TEST_LOG_DATA)
  def test_constructor_counts_lines(self, open_, *stubs):
    fix_iteration_in_mock_open(open_)
    
    log = Log(TEST_LOG_PATH)
    self.assertEqual(TEST_LOG_DATA_LINE_CNT, log.get_line_count())

  @patch('builtins.open', new_callable=mock_open, read_data=TEST_LOG_DATA)
  def test__count_lines_in_file_counts_lines(self, open_):
    fix_iteration_in_mock_open(open_)
  
    line_count = Log._count_lines_in_file(TEST_LOG_PATH)
    open_.assert_called_with(TEST_LOG_PATH, 'r')
    self.assertEqual(line_count, TEST_LOG_DATA_LINE_CNT)
    
  @patch('os.path.isfile', return_value=False)
  def test__count_lines_in_file_raises_if_file_does_not_exist(self, *stubs):
    with self.assertRaises(FileNotFoundError):
      Log._count_lines_in_file('file.log')
  
  @patch('os.path.getsize', return_value=TEST_LOG_DATA_SIZE)
  @patch('builtins.open', new_callable=mock_open, read_data=TEST_LOG_DATA)
  @patch('toolbag.logkeep.Log._raise_if_not_a_file')
  @patch('shutil.copy2')
  def test_clone_to_a_backup_default(self, copy2_mock, *stubs):
    log = Log(TEST_LOG_PATH)
    log.clone_to_a_backup()
    copy2_mock.assert_called_with(TEST_LOG_PATH, TEST_LOG_PATH+'.prev')

  @patch('os.path.getsize', return_value=TEST_LOG_DATA_SIZE)
  @patch('builtins.open', new_callable=mock_open, read_data=TEST_LOG_DATA)
  @patch('toolbag.logkeep.Log._raise_if_not_a_file')
  @patch('shutil.copy2')
  def test_clone_to_a_backup_with_user_defined_path(self, copy2_mock, *stubs):
    log = Log(TEST_LOG_PATH)
    log.clone_to_a_backup(TEST_USER_DEFINED_CLONE_PATH)
    copy2_mock.assert_called_with(TEST_LOG_PATH, TEST_USER_DEFINED_CLONE_PATH)

  @patch('os.path.isfile', return_value=False)
  def test__raise_if_not_a_file_raises_on_bad_directory(self, *stubs):
    with self.assertRaises(FileNotFoundError):
      Log._raise_if_not_a_file('./')

  @patch('os.path.isfile', return_value=False)
  @patch('toolbag.logkeep.Log._raise_if_not_a_file')
  @patch('toolbag.logkeep.Log._count_lines_in_file')
  @patch('os.path.getsize', return_value=TEST_LOG_DATA_SIZE)
  def test_clear_original_file_raises_on_not_a_file(self, *args):
    log = Log('file.log')
  
    with self.assertRaises(FileNotFoundError):
      log.clear_original_file()
  
  @patch('os.path.isfile', return_value=True)
  @patch('os.path.getsize', return_value=TEST_LOG_DATA_SIZE)
  @patch('builtins.open', new_callable=mock_open, read_data=TEST_LOG_DATA)
  @patch('toolbag.logkeep.Log._clear_file_contents')
  def test_clear_original_file_clears_data(self, clear_mock, *args):
    log = Log('file.log')
    log.clear_original_file()
    
    clear_mock.assert_called_with('file.log')
  
  @patch('os.remove')
  @patch('os.rmdir')
  @patch('os.unlink')
  @patch('shutil.rmtree')
  @patch('builtins.open', new_callable=mock_open, read_data=TEST_LOG_DATA)
  @patch('os.path.isfile', return_value=True)
  @patch('os.path.getsize', return_value=TEST_LOG_DATA_SIZE)
  def test_clear_original_file_does_not_try_to_delete_the_file(self, get_size_mock, 
                                            isfile_mock, open_, *remove_func_mocks):
    log = Log('file.log')
    log.clear_original_file()
  
    # Make sure we actually have the mocks we expect since failure here would corrupt our test.
    self.assertTrue(len(remove_func_mocks) > 0)
    
    for func in remove_func_mocks:
      func.assert_not_called()
  
  @patch('os.path.isfile', return_value=True)
  @patch('builtins.open', new_callable=mock_open, read_data=TEST_LOG_DATA)
  def test__clear_file_contents_clears_file(self, open_, *args):
    Log._clear_file_contents('file.log')
    open_.assert_called_with('file.log', 'w')
    open_().close.assert_called()
    open_().write.assert_not_called()
    
  @patch('os.path.isfile', return_value=False)
  @patch('builtins.open', new_callable=mock_open, read_data=TEST_LOG_DATA)
  def test__clear_file_contents_raises_and_does_not_open_file(self, open_, *args):
    with self.assertRaises(FileNotFoundError):
      Log._clear_file_contents('file.log')
    
    open_.assert_not_called()
    