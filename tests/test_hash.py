import unittest
from unittest.mock import MagicMock, mock_open, patch

import hashlib

from toolbag import hash

TEST_DATA_RAW = 'some data'.encode()
TEST_DATA_MD5 = '1e50210a0202497fb79bc38b6ade6c34'
TEST_DATA_SHA256 = '1307990e6ba5ca145eb35e99182a9bec46531bc54ddf656a602c780fa0240dee'
TEST_FILE_PATH = '/path/to/file'
TEST_STRING = 'THIS IS A TEST STRING'
TEST_FILE_NAME = 'thisisonlyatest.txt'

class FileHash_Class_TestCase(unittest.TestCase):
  @patch('toolbag.hash.hash_file_in_chunks_to_hex_str', return_value=TEST_STRING)
  def test_constructor_sets_member_vars_and_computes_hash(self, hash_func_mock):
    mock_hash_object = MagicMock()
    TEST_HASH_NAME = 'MD5'
    TEST_FILENAME = 'test.txt'
    
    fn = hash.FileHash(TEST_HASH_NAME, mock_hash_object, TEST_FILENAME)
    self.assertEqual(fn.hash_name, TEST_HASH_NAME)
    self.assertEqual(fn.hash_string, TEST_STRING)
    hash_func_mock.assert_called_with(TEST_FILENAME, mock_hash_object)
    
  @patch('toolbag.hash.hash_file_in_chunks_to_hex_str', return_value=TEST_STRING)
  def test__str__func(self, hash_func_mock):
    mock_hash_object = MagicMock()
    TEST_HASH_NAME = 'MD5'
    TEST_FILENAME = 'test.txt'
    
    fn = hash.FileHash(TEST_HASH_NAME, mock_hash_object, TEST_FILENAME)
    self.assertEqual(str(fn), f'{TEST_HASH_NAME:<10}{TEST_STRING}')

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
    
class HashModuleFunctions_TestCase(unittest.TestCase):
  @patch('sys.exit')
  def test__exit_if_no_file_exists_exits_with_no_file(self, exit_mock):
    hash._exit_if_no_file_exists(TEST_FILE_NAME)
    exit_mock.assert_called()
  
  @patch('os.path.isfile', return_value=True)
  @patch('sys.exit')
  def test__exit_if_no_file_exists_does_not_exit_with_file(self, exit_mock, isfile_mock):
    hash._exit_if_no_file_exists(TEST_FILE_NAME)
    isfile_mock.assert_called_with(TEST_FILE_NAME)
    exit_mock.assert_not_called()
    
  def test__get_all_supported_hashes_returns_supported_hashes(self):
    self.assertEqual(hash._SUPPORTED_HASHES.keys(), hash._get_all_supported_hashes())
    
  #def test__get_selected_algorithms_returns_all_supported_on_none(self):
  #def test__get_selected_algorithms_splits_args_on_commas(self):
  #def test__get_supported_hashes_str_returns_all_supported_hashes(self):
  #def test__main_exits_instead_of_excepting_on_nonexistent_file(self):
  #def test__build_argument_parser_contains_required_arguments(self):