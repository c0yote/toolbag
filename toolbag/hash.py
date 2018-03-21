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

class FileHashRenderer:
  def __init__(self, hash_name, hash_object, filename):
    self.hash_name = hash_name
    self.hash_string = hash_file_in_chunks_to_hex_str(filename, hash_object)
    
  def __str__(self):
    return f'{self.hash_name:<10}{self.hash_string}'

_LABEL = 0
_HASH_OBJECT_CONSTRUCTOR = 1
_SUPPORTED_HASHES = {
  'md5': ('MD5', hashlib.md5),
  'sha256': ('SHA256', hashlib.sha256),
}

def _build_hash_renderers(filename, alg_args=None):
  if alg_args:
    algorithms = args.algs.split(',')
  else:
    algorithms = ['md5', 'sha256']
  
  renderers = list()
  if 'md5' in algorithms:
    renderers.append(FileHashRenderer('MD5', hashlib.md5(), filename))
  if 'sha256' in algorithms:
    renderers.append(FileHashRenderer('SHA256', hashlib.sha256(), filename))

  return renderers
  
def _confirm_file_exists(filename):
  if not os.path.isfile(filename):
    sys.exit('Could not locate file: \''+filename+'\'')
  
def _main(args):
  _confirm_file_exists(args.file)
  
  for r in _build_hash_renderers(args.file, args.algs):
    print(r)
  
def _build_argument_parser():
  DESCRIPTION = 'Compute the hash of a file.'
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
    