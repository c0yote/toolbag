import argparse
import hashlib
import math
import os.path
import sys

DEFAULT_HASHING_CHUNK_SIZE = int(math.pow(2,16))

def hash_file_in_chunks_to_hex_str(filename, hash_object, 
                        chunk_size=DEFAULT_HASHING_CHUNK_SIZE):
  with open(filename, 'rb') as file:
    chunk = file.read(chunk_size)
    while chunk:
      hash_object.update(chunk)
      chunk = file.read(chunk_size)
  return hash_object.hexdigest()

  
class _FileHash:
  def __init__(self, hash_name, hash_object, filename):
    self.hash_name = hash_name
    self.hash_str = hash_file_in_chunks_to_hex_str(filename, hash_object)
    
  def __str__(self):
    return f'{self.hash_name:<10}{self.hash_str}'

    
class _Application:
  LABEL = 0
  HASH_OBJECT_CONSTRUCTOR = 1
  # Adding a hash to this dict automatically implements functional, argument, 
  # and help listing support for it.
  SUPPORTED_HASHES = {
    'md5': ('MD5', hashlib.md5),
    'sha1': ('SHA1', hashlib.sha1),
    'sha256': ('SHA256', hashlib.sha256),
  }

  def __init__(self):
    arg_parser = self.build_argument_parser()
    self.args = arg_parser.parse_args()
    self.filename = self.args.file
    self.selected_algs = self.get_selected_algorithms()
    
  def run(self):
    self.exit_if_no_file_exists()
    self.hashes = self.compute_hashes()
    
    for hash in self.hashes:
      print(hash)
  
  def build_argument_parser(self):
    ARG_FILE_HELP = 'The file to hash.'
    ARG_ALGS_HELP = 'choose hashing algorithms to use (ex. --algs=md5,sha256)'
    description = _Application.get_description()
    
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('file', help=ARG_FILE_HELP)
    parser.add_argument('--algs', help=ARG_ALGS_HELP, type=str)
    return parser
  
  def exit_if_no_file_exists(self):
    if not os.path.isfile(self.filename):
      sys.exit('Could not locate file: \''+self.filename+'\'')
  
  def get_selected_algorithms(self):
    algorithm_args = self.args.algs
    if algorithm_args:
      return algorithm_args.split(',')
    else:
      return _Application.get_all_supported_algorithms()
  
  def compute_hashes(self):
    hashes = list()
    for alg in self.selected_algs:
      hash_alg = _Application.SUPPORTED_HASHES[alg]
      label = hash_alg[_Application.LABEL]
      hash_obj = hash_alg[_Application.HASH_OBJECT_CONSTRUCTOR]()
      
      hashes.append(_FileHash(label, hash_obj, self.filename))
      
    return hashes

  @staticmethod
  def get_description():
    algorithm_list = _Application.get_supported_hashes_str()
    return f'Compute the hash of a file. Supports: {algorithm_list}'
  
  @staticmethod
  def get_all_supported_algorithms():
    return _Application.SUPPORTED_HASHES.keys()
  
  @staticmethod
  def get_supported_hashes_str():
    hashes_list_str = ''
    for k,v in _Application.SUPPORTED_HASHES.items():
      hashes_list_str += k + ' '

    hashes_list_str = hashes_list_str.rstrip()
    
    return hashes_list_str


if __name__ == '__main__':
  app = _Application()
  app.run()
  