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

class FileHash:
  def __init__(self, hash_name, hash_object, filename):
    self.hash_name = hash_name
    self.hash_string = hash_file_in_chunks_to_hex_str(filename, hash_object)
    
  def __str__(self):
    return f'{self.hash_name:<10}{self.hash_string}'

_LABEL = 0
_HASH_OBJECT_CONSTRUCTOR = 1
# Adding a hash to this dict automatically implements complete support for it.
_SUPPORTED_HASHES = {
  'md5': ('MD5', hashlib.md5),
  'sha1': ('SHA1', hashlib.sha1),
  'sha256': ('SHA256', hashlib.sha256),
}

def _build_hashes(filename, selected_algorithms):
  hashes = list()
  for alg in selected_algorithms:
    hash_alg = _SUPPORTED_HASHES[alg]
    label = hash_alg[_LABEL]
    hash_obj = hash_alg[_HASH_OBJECT_CONSTRUCTOR]()
    
    hashes.append(FileHash(label, hash_obj, filename))

  return hashes
  
def _confirm_file_exists(filename):
  if not os.path.isfile(filename):
    sys.exit('Could not locate file: \''+filename+'\'')

def _get_all_supported_hashes():
  return _SUPPORTED_HASHES.keys()
    
def _get_selected_algorithms(alg_args):
  if alg_args:
    selected_algorithms = args.algs.split(',')
  else:
    selected_algorithms = _get_all_supported_hashes()
    
  return selected_algorithms
    
def _get_supported_hashes_str():
  hashes_list_str = ''
  for k,v in _SUPPORTED_HASHES.items():
    hashes_list_str += ' ' + k

  return hashes_list_str
    
def _main(args):
  _confirm_file_exists(args.file)
  
  filename = args.file
  selected_algs = _get_selected_algorithms(args.algs)
  
  for r in _build_hashes(filename, selected_algs):
    print(r)
  
def _build_argument_parser():
  DESCRIPTION = 'Compute the hash of a file. Supports: '+_get_supported_hashes_str()
  ARG_FILE_HELP = 'The file to hash.'
  ARG_ALGS_HELP = 'choose hashing algorithms to use (ex. --algs=md5,sha256)'
  
  parser = argparse.ArgumentParser(description=DESCRIPTION)
  parser.add_argument('file', help=ARG_FILE_HELP)
  parser.add_argument('--algs', help=ARG_ALGS_HELP, type=str)
  parser.set_defaults(func=_main)
  return parser
  
if __name__ == '__main__':
  arg_parser = _build_argument_parser()
  args = arg_parser.parse_args()
  args.func(args)
    