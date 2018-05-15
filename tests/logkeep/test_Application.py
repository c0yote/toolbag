import os
import unittest
from unittest import skip
from unittest.mock import MagicMock, mock_open, patch
  
from toolbag.logkeep import _Application, main

TEST_LOG_PATH = '/some/path/to/log.log'
TEST_ERROR_RETURN = 'Some error occurred'
TEST_LIMIT_VALUE_A = 10
TEST_LIMIT_VALUE_B = 11
TEST_LIMIT_VALUE_C = 0.5
TEST_LIMIT_GREATER = 12
TEST_LIMIT_GREATER_FLOAT = 0.6
TEST_ARGS = ['app', TEST_LOG_PATH]
TEST_SIZE_ARGS = ['app', '--size_limit', f'{TEST_LIMIT_VALUE_A}', TEST_LOG_PATH]
TEST_SIZE_FLOAT_ARGS = ['app', '--size_limit', f'{TEST_LIMIT_VALUE_C}', TEST_LOG_PATH]
TEST_SIZE_ARGS = ['app', '--size_limit', f'{TEST_LIMIT_VALUE_A}', TEST_LOG_PATH]
TEST_LINE_ARGS = ['app', '--line_limit', f'{TEST_LIMIT_VALUE_B}', TEST_LOG_PATH]
TEST_SIZE_AND_LINE_ARGS = ['app', '--size_limit', f'{TEST_LIMIT_VALUE_A}', 
                            '--line_limit', f'{TEST_LIMIT_VALUE_B}',
                            TEST_LOG_PATH]
TEST_UNHANDLED_EXCEPTION_OBJ = Exception(TEST_ERROR_RETURN)
    
class Application_TestCase(unittest.TestCase):
  @patch('sys.argv', TEST_SIZE_ARGS)
  @patch('toolbag.logkeep.Log')
  def test_size_threshold_storage(self, *stubs):
    app = _Application()
    self.assertEqual(app._size_limit_mb, TEST_LIMIT_VALUE_A)
    self.assertEqual(app._line_limit, None)
    
  @patch('sys.argv', TEST_SIZE_FLOAT_ARGS)
  @patch('toolbag.logkeep.Log')
  def test_size_threshold_storage_with_float(self, *stubs):
    app = _Application()
    self.assertEqual(app._size_limit_mb, TEST_LIMIT_VALUE_C)
    self.assertEqual(app._line_limit, None)
    
  @patch('sys.argv', TEST_LINE_ARGS)
  @patch('toolbag.logkeep.Log')
  def test_line_threshold_storage(self, *stubs):
    app = _Application()
    self.assertEqual(app._size_limit_mb, None)
    self.assertEqual(app._line_limit, TEST_LIMIT_VALUE_B)
  
  @patch('sys.argv', TEST_SIZE_AND_LINE_ARGS)
  @patch('toolbag.logkeep.Log')
  def test_size_and_line_threshold_storage(self, *stubs):
    app = _Application()
    self.assertEqual(app._size_limit_mb, TEST_LIMIT_VALUE_A)
    self.assertEqual(app._line_limit, TEST_LIMIT_VALUE_B)
    
  @patch('sys.argv', TEST_ARGS)
  @patch('toolbag.logkeep.Log')
  def test_no_threshold_storage(self, *stubs):
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
    
  @patch('sys.argv', TEST_SIZE_FLOAT_ARGS)
  @patch('toolbag.logkeep.Log')
  def test_clones_log_on_size_threshold_with_float(self, log_mock):
    handle = log_mock()
    handle.get_file_size_in_megabytes.return_value = TEST_LIMIT_GREATER_FLOAT
  
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
  def test_clones_log_on_size_and_line_count_threshold(self, log_mock):
    handle = log_mock()
    handle.get_line_count.return_value = TEST_LIMIT_GREATER
  
    app = _Application()
    app.run()
    
    handle.clone_to_a_backup.assert_called_with()
    
  @patch('sys.argv', TEST_ARGS)
  @patch('toolbag.logkeep.Log', side_effect=PermissionError(TEST_ERROR_RETURN))
  def test_constructor_raises_runtimeerror_on_bad_permissions(self, *args):
    with self.assertRaises(RuntimeError) as e:
      _Application()
    
  @patch('sys.argv', TEST_ARGS)
  @patch('toolbag.logkeep.Log', side_effect=FileNotFoundError(TEST_ERROR_RETURN))
  def test_constructor_raises_runtimeerror_on_file_not_found(self, *args):
    with self.assertRaises(RuntimeError) as e:
      _Application()
  
  @patch('sys.argv', TEST_SIZE_ARGS)
  @patch('toolbag.logkeep.Log')
  def test_run_raises_runtimeerror_on_bad_permissions(self, log_mock, *args):
    handle = log_mock()
    handle.clone_to_a_backup.side_effect = PermissionError(TEST_ERROR_RETURN)
    handle.get_file_size_in_megabytes.return_value = TEST_LIMIT_GREATER
  
    app = _Application()
    with self.assertRaises(RuntimeError) as e:
      app.run()
    
  @patch('toolbag.logkeep.Log')
  @patch('sys.argv', TEST_SIZE_ARGS)
  def test_run_raises_runtimeerror_on_file_not_found(self, log_mock, *args):
    handle = log_mock()
    handle.clone_to_a_backup.side_effect = FileNotFoundError(TEST_ERROR_RETURN)
    handle.get_file_size_in_megabytes.return_value = TEST_LIMIT_GREATER
    app = _Application()
    with self.assertRaises(RuntimeError) as e:
      app.run()
    
class logkeep_main_TestCase(unittest.TestCase):
  @patch('toolbag.logkeep._Application', side_effect=RuntimeError(TEST_ERROR_RETURN))
  @patch('sys.argv', TEST_ARGS)
  @patch('builtins.print')
  def test_main_handles_runtime_errors_from_application_constructor(self, print_mock, *args):
    main()  
    print_mock.assert_called_with('Error: '+TEST_ERROR_RETURN)
  
  @patch('toolbag.logkeep._Application.run', side_effect=RuntimeError(TEST_ERROR_RETURN))
  @patch('toolbag.logkeep.Log')
  @patch('sys.argv', TEST_ARGS)
  @patch('builtins.print')
  def test_main_handles_runtime_errors_from_application_run(self, print_mock, *args):
    main()  
    print_mock.assert_called_with('Error: '+TEST_ERROR_RETURN)

  @patch('toolbag.logkeep._Application', side_effect=TEST_UNHANDLED_EXCEPTION_OBJ)
  @patch('sys.argv', TEST_ARGS)
  @patch('builtins.print')
  def test_main_handles_unhandled_exceptions_from_application_constructor(self, print_mock, *args):
    main()  
    print_mock.assert_called_with('Unhandled Exception: '+repr(TEST_UNHANDLED_EXCEPTION_OBJ))
  
  @patch('toolbag.logkeep._Application.run', side_effect=TEST_UNHANDLED_EXCEPTION_OBJ)
  @patch('toolbag.logkeep.Log')
  @patch('sys.argv', TEST_ARGS)
  @patch('builtins.print')
  def test_main_handles_unhandled_exceptions_from_application_run(self, print_mock, *args):
    main()  
    print_mock.assert_called_with('Unhandled Exception: '+repr(TEST_UNHANDLED_EXCEPTION_OBJ))
    