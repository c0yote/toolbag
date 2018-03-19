import unittest
from unittest.mock import MagicMock, mock_open, patch

import hashlib

from toolbag import hash

TEST_DATA_RAW = 'some data'.encode()
TEST_DATA_MD5 = '1e50210a0202497fb79bc38b6ade6c34'
TEST_DATA_SHA256 = '1307990e6ba5ca145eb35e99182a9bec46531bc54ddf656a602c780fa0240dee'
TEST_FILE_PATH = '/path/to/file'

class HashFileToHexStrInChunksFuncTestCase(unittest.TestCase):
  
  @patch('builtins.open', new_callable=mock_open, read_data=TEST_DATA_RAW)
  def test_returns_hash_strings(self, mock_file):
    hash_object = hashlib.md5()
    self.assertEqual(
      hash.hash_file_to_hex_str_in_chunks(TEST_FILE_PATH, hash_object),
      TEST_DATA_MD5)
      
    hash_object = hashlib.sha256()
    self.assertEqual(
      hash.hash_file_to_hex_str_in_chunks(TEST_FILE_PATH, hash_object),
      TEST_DATA_SHA256)
    
  @patch('builtins.open', new_callable=mock_open, read_data=TEST_DATA_RAW)
  def test_opens_file_rb_mode(self, mock_file):
    mock_hash_object = MagicMock()
    hash.hash_file_to_hex_str_in_chunks(TEST_FILE_PATH, mock_hash_object)
    mock_file.assert_called_with(TEST_FILE_PATH, 'rb')
  
  def test_uses_default_buffer_size(self):
    mock_file = MagicMock()
    with patch('builtins.open', mock_open(mock_file, read_data=TEST_DATA_RAW)) as the_mock_open:
    
      mock_hash_object = MagicMock()
      hash.hash_file_to_hex_str_in_chunks(TEST_FILE_PATH, mock_hash_object)
      mock_file.read.assert_called_with(hash.DEFAULT_HASHING_BUFFER_SIZE)
      print('outside: '+str(mock_file))
    
  #def test_setting_chunk_size