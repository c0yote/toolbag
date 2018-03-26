import unittest
from unittest.mock import MagicMock, mock_open, patch

import hashlib

from toolbag import hash

TEST_DATA_RAW = 'some data'.encode()
TEST_DATA_MD5 = '1e50210a0202497fb79bc38b6ade6c34'
TEST_DATA_SHA256 = '1307990e6ba5ca145eb35e99182a9bec46531bc54ddf656a602c780fa0240dee'
TEST_FILE_PATH = '/path/to/file'
TEST_STRING = 'THIS IS A TEST STRING'
TEST_SIMPLE_ARGS = ['app', TEST_FILE_PATH]
TEST_HASH_CHOICE_ARGS = ['app', '--algs=md5,sha1', TEST_FILE_PATH]
TEST_ARG_SELECTED_ALGS = ['md5', 'sha1']

class FileHash_Class_TestCase(unittest.TestCase):
  @patch('toolbag.hash.hash_file_in_chunks_to_hex_str', return_value=TEST_STRING)
  def test_constructor_sets_member_vars_and_computes_hash(self, hash_func_mock):
    mock_hash_object = MagicMock()
    TEST_HASH_NAME = 'MD5'
    TEST_FILENAME = 'test.txt'
    
    fn = hash._FileHash(TEST_HASH_NAME, mock_hash_object, TEST_FILENAME)
    self.assertEqual(fn.hash_name, TEST_HASH_NAME)
    self.assertEqual(fn.hash_str, TEST_STRING)
    hash_func_mock.assert_called_with(TEST_FILENAME, mock_hash_object)
    
  @patch('toolbag.hash.hash_file_in_chunks_to_hex_str', return_value=TEST_STRING)
  def test__str__func(self, hash_func_mock):
    mock_hash_object = MagicMock()
    TEST_HASH_NAME = 'MD5'
    TEST_FILENAME = 'test.txt'
    
    fn = hash._FileHash(TEST_HASH_NAME, mock_hash_object, TEST_FILENAME)
    self.assertEqual(str(fn), f'{TEST_HASH_NAME:<10}{TEST_STRING}')

class HashApplication_Class_TestCase(unittest.TestCase):
  @patch('sys.argv', TEST_SIMPLE_ARGS)
  @patch('os.path.isfile', return_value=False)
  @patch('sys.exit')
  def test_exit_if_no_file_exists_exits_with_no_file(self, exit_mock, isfile_mock):
    app = hash._Application()
    app.exit_if_no_file_exists()
    isfile_mock.assert_called_with(TEST_FILE_PATH)
    exit_mock.assert_called()
  
  @patch('sys.argv', TEST_SIMPLE_ARGS)
  @patch('os.path.isfile', return_value=True)
  @patch('sys.exit')
  def test_exit_if_no_file_exists_does_not_exit_with_file(self, exit_mock, isfile_mock):
    app = hash._Application()
    app.exit_if_no_file_exists()
    isfile_mock.assert_called_with(TEST_FILE_PATH)
    exit_mock.assert_not_called()
  
  @patch('sys.argv', TEST_SIMPLE_ARGS)
  def test_get_all_supported_algorithms_returns_supported_hash_algorithms(self):
    app = hash._Application()
    self.assertEqual(hash._Application.SUPPORTED_HASHES.keys(), 
                     app.get_all_supported_algorithms())
  
  @patch('sys.argv', TEST_SIMPLE_ARGS)
  @patch('toolbag.hash._Application.compute_hashes')
  @patch('toolbag.hash._Application.exit_if_no_file_exists')
  def test_run_checks_for_file_existence(self, file_exit_mock, comp_hash_stub):
    app = hash._Application()
    app.run()
    file_exit_mock.assert_called()
  
  @patch('sys.argv', TEST_SIMPLE_ARGS)
  def test_get_selected_algorithms_returns_all_supported_on_none(self):
    app = hash._Application()
    self.assertEqual(app.selected_algs, hash._Application.get_all_supported_algorithms())

  @patch('sys.argv', TEST_HASH_CHOICE_ARGS)
  def test_get_selected_algorithms_returns_arg_selected_algorithms(self):
    app = hash._Application()
    self.assertEqual(app.selected_algs, TEST_ARG_SELECTED_ALGS)
  
  def test_get_supported_hashes_str_returns_all_supported_hashes(self):
    hash_list_str = hash._Application.get_supported_hashes_str()
    supported_hashes = hash_list_str.split(' ')
    for hash_name in supported_hashes:
      self.assertTrue(hash_name in hash._Application.SUPPORTED_HASHES)
  
  #TODO def test_build_argument_parser_contains_required_arguments(self, add_arg_mock):
    
class HashFileInChunksToHexStr_Func_TestCase(unittest.TestCase):
  @patch('builtins.open', new_callable=mock_open, read_data=TEST_DATA_RAW)
  def test_returns_hash_strings(self, open_):
    hash_object = hashlib.md5()
    self.assertEqual(
      hash.hash_file_in_chunks_to_hex_str(TEST_FILE_PATH, hash_object),
      TEST_DATA_MD5)
      
    hash_object = hashlib.sha256()
    self.assertEqual(
      hash.hash_file_in_chunks_to_hex_str(TEST_FILE_PATH, hash_object),
      TEST_DATA_SHA256)
    
  @patch('builtins.open', new_callable=mock_open, read_data=TEST_DATA_RAW)
  def test_opens_file_rb_mode(self, open_):
    mock_hash_object = MagicMock()
    hash.hash_file_in_chunks_to_hex_str(TEST_FILE_PATH, mock_hash_object)
    open_.assert_called_with(TEST_FILE_PATH, 'rb')
  
  @patch('builtins.open', new_callable=mock_open, read_data=TEST_DATA_RAW)
  def test_uses_default_buffer_size(self, open_):
    mock_hash_object = MagicMock()
    hash.hash_file_in_chunks_to_hex_str(TEST_FILE_PATH, mock_hash_object)
    handle = open_()
    handle.read.assert_called_with(hash.DEFAULT_HASHING_CHUNK_SIZE)
    
  @patch('builtins.open', new_callable=mock_open, read_data=TEST_DATA_RAW)
  def test_setting_chunk_size_set(self, open_):
    TEST_BUFFER_SIZE_VALUE = 123456789
    mock_hash_object = MagicMock()
    hash.hash_file_in_chunks_to_hex_str(TEST_FILE_PATH, mock_hash_object, TEST_BUFFER_SIZE_VALUE)
    handle = open_()
    handle.read.assert_called_with(TEST_BUFFER_SIZE_VALUE)
