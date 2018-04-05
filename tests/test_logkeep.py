import unittest
from unittest.mock import MagicMock, mock_open, patch

import os

from toolbag.logkeep import Log

TEST_LOG_PATH = '/some/path/to/log.log'
TEST_LOG_DATA = f'line 0{os.linesep}line 1{os.linesep} line 2'
TEST_LOG_DATA_SIZE = len(TEST_LOG_DATA.encode('utf-8'))
TEST_LOG_DATA_LINE_CNT = 3
TEST_USER_DEFINED_CLONE_PATH = '/user/path/to/log.bak'

def fix_iteration_in_mock_open(open_mock):
  open_mock.return_value.__iter__ = lambda self : iter(self.readline, '')

class Log_TestCase(unittest.TestCase):
  """ When we don't care about the mocks generated during patching, '*args' is 
      used in the test function parameters so there isn't a long list of useless 
      patch parameters taking up space.
  """

  def test_constructor_excepts_on_no_file(self):
    with self.assertRaises(FileNotFoundError):
      log = Log(TEST_LOG_PATH)
  
  @patch('os.path.getsize', return_value=TEST_LOG_DATA_SIZE)
  @patch('builtins.open', new_callable=mock_open, read_data=TEST_LOG_DATA)
  def test_constructor_computes_size(self, *args):
    log = Log(TEST_LOG_PATH)
    self.assertEqual(TEST_LOG_DATA_SIZE, log.get_file_size_in_bytes())

  @patch('os.path.getsize', return_value=TEST_LOG_DATA_SIZE)
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
  @patch('shutil.copy2')
  def test_clone_to_a_backup_default(self, copy2_mock, *args):
    log = Log(TEST_LOG_PATH)
    log.clone_to_a_backup()
    copy2_mock.assert_called_with(TEST_LOG_PATH, TEST_LOG_PATH+'.prev')

  @patch('os.path.getsize', return_value=TEST_LOG_DATA_SIZE)
  @patch('builtins.open', new_callable=mock_open, read_data=TEST_LOG_DATA)
  @patch('shutil.copy2') 
  def test_clone_to_a_backup_wiht_user_defined_path(self, copy2_mock, *args):
    log = Log(TEST_LOG_PATH)
    log.clone_to_a_backup(TEST_USER_DEFINED_CLONE_PATH)
    copy2_mock.assert_called_with(TEST_LOG_PATH, TEST_USER_DEFINED_CLONE_PATH)
    