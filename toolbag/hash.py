import hashlib
import math

DEFAULT_HASHING_BUFFER_SIZE = int(math.pow(2,16))

def hash_file_to_hex_str_in_chunks(filename, hash_object, 
                        buffer_size=DEFAULT_HASHING_BUFFER_SIZE):
  with open(filename, 'rb') as file:
    print('inside: '+str(file))
    chunk = file.read(buffer_size)
    while chunk:
      hash_object.update(chunk)
      chunk = file.read(buffer_size)
  return hash_object.hexdigest()

def _get_parsed_arguments():
  import argparse
  parser = argparse.ArgumentParser(description='Compute the hash of a file.')
  parser.add_argument('file', help='The file to hash.')
  parser.add_argument('--md5', help='Compute an MD5 hash of the file.', 
                      action="store_true")
  parser.add_argument('--sha256', help='Compute an SHA-256 hash of the file.', 
                      action="store_true")
  return parser.parse_args()
  
if __name__ == '__main__':
  LEFT_COLUMN_WIDTH = 12

  parsed_args = _get_parsed_arguments()
  filename = parsed_args.file
  compute_md5 = parsed_args.md5
  compute_sha256 = parsed_args.sha256
  compute_all = not compute_md5 and not compute_sha256
  
  try:
    if compute_md5 or compute_all:
      hash_object = hashlib.md5()
      hash_string = hash_file_to_hex_str_in_chunks(filename, hash_object)
      print('MD5: '.ljust(LEFT_COLUMN_WIDTH)+hash_string)
    if compute_sha256 or compute_all:
      hash_object = hashlib.sha256()
      hash_string = hash_file_to_hex_str_in_chunks(filename, hash_object)
      print('SHA-256: '.ljust(LEFT_COLUMN_WIDTH)+hash_string)
  except FileNotFoundError:
    print('Could not locate file: \''+parsed_args.file+'\'', file=sys.stderr)
    