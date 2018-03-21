import unittest
from unittest.mock import MagicMock, mock_open, patch

import hashlib

from toolbag import hash

TEST_DATA_RAW = 'some data'.encode()
TEST_DATA_MD5 = '1e50210a0202497fb79bc38b6ade6c34'
TEST_DATA_SHA256 = '1307990e6ba5ca145eb35e99182a9bec46531bc54ddf656a602c780fa0240dee'
TEST_FILE_PATH = '/path/to/file'

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