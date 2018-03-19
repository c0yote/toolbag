import argparse
import hashlib
import math
import sys

DEFAULT_HASHING_BUFFER_SIZE = int(math.pow(2,16))

def hash_file_in_chunks_to_hex_str(filename, hash_object, 
                        buffer_size=DEFAULT_HASHING_BUFFER_SIZE):
  with open(filename, 'rb') as file:
    chunk = file.read(buffer_size)
    while chunk:
      hash_object.update(chunk)
      chunk = file.read(buffer_size)
  return hash_object.hexdigest()

def _display_hash(label, hash):
  print(f'{label:<12}{hash}')
  
def _md5(filename):
  hash_object = hashlib.md5()
  hash_string = hash_file_in_chunks_to_hex_str(filename, hash_object)
  _display_hash('MD5',hash_string)
  
def _sha256(filename):
  hash_object = hashlib.sha256()
  hash_string = hash_file_in_chunks_to_hex_str(filename, hash_object)
  _display_hash('SHA-256',hash_string)
  
def main(args):
  filename = args.file
  compute_md5 = args.md5
  compute_sha256 = args.sha256
  compute_all = not compute_md5 and not compute_sha256
  
  try:
    if compute_md5 or compute_all:
      _md5(filename)
    if compute_sha256 or compute_all:
      _sha256(filename)
      
  except FileNotFoundError:
    print('Could not locate file: \''+args.file+'\'', file=sys.stderr)
  
def _build_argument_parser():
  DESCRIPTION = 'Compute the hash of a file.'
  ARG_FILE_HELP = 'The file to hash.'
  ARG_MD5_HELP = 'Compute an MD5 hash of the file.'
  ARG_SHA256_HELP = 'Compute an SHA-256 hash of the file.'
  
  parser = argparse.ArgumentParser(description=DESCRIPTION)
  parser.add_argument('file', help=ARG_FILE_HELP)
  parser.add_argument('--md5', help=ARG_MD5_HELP, action="store_true")
  parser.add_argument('--sha256', help=ARG_SHA256_HELP, action="store_true")
  parser.set_defaults(func=main)
  return parser
  
if __name__ == '__main__':
  arg_parser = _build_argument_parser()
  args = arg_parser.parse_args()
  args.func(args)
    