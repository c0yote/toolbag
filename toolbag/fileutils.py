from datetime import datetime
import hashlib
from functools import partial
import multiprocessing
import os
import shutil
import time

from hash import hash_file_in_chunks_to_hex_str

# Good Idea Fairy
# - Argument to make non-recursive.
# - Add runtime.

# Replace with a progress bar class.
files_hashed_count = 0

def hash_file_to_hex_str(filename):
  return hash_file_in_chunks_to_hex_str(filename, hashlib.md5())

def hash_file_to_hash_file_tuple(filename):
  return (hash_file_to_hex_str(filename), filename)

def _get_file_unrepresented_in_archive(archive_hash_list, filename):
  hash_string = hash_file_in_chunks_to_hex_str(filename, hashlib.md5())
  if hash_string not in archive_hash_list:
    return filename

def _build_filename_list_recursively(directory):
  filename_list = list()
  for root, directories, filenames in os.walk(directory):
    for filename in filenames:
      filename_list.append(os.path.join(root, filename))
  return filename_list
  
def _build_file_hash_tuples_from_files(filenames, jobs=1):
  proc_pool = multiprocessing.Pool(processes=jobs)
  hash_list = proc_pool.map(hash_file_to_hash_file_tuple, filenames)
  proc_pool.close()
  
  return hash_list
  
def _dupl_main(args):
  print('Searching for duplicates...')
  filenames = _build_filename_list_recursively(args.dir)
  print('  Located ['+str(len(filenames))+'] files for testing.')
  
  file_hash_tuple_list = _build_file_hash_tuples_from_files(filenames, args.jobs)
  
  print('  Hash computation complete.')
  
  hash_dict = dict()
  
  HASH = 0
  FILENAME = 1
  for entry in file_hash_tuple_list:
    if entry[HASH] not in hash_dict:
      hash_dict[entry[HASH]] = [entry[FILENAME]]
    else:
      hash_dict[entry[HASH]].append(entry[FILENAME])

  print('  Found Duplicates:')
  for k,v in hash_dict.items():
    if len(v) > 1:
      print('    '+str(v))
  
def _evac_main(args):
  while True:
    print('Waiting for data to mount.')
    while not os.path.isdir(args.mondir):
      time.sleep(1)
      
    print('Copying files.')
    dest_path = os.path.join(args.dest, datetime.now().strftime("%Y-%m-%d %H_%M_%S"))
    shutil.copytree(args.mondir, dest_path)
    print('Copy complete.')
    
    print('Waiting for unmount.')
    while os.path.isdir(args.mondir):
      time.sleep(1)    
  
def _repr_main(args):
  print('Checking for representation...')
  reference_filenames = _build_filename_list_recursively(args.refdir)
  evaluation_filenames = _build_filename_list_recursively(args.evaldir)
  
  print('  Located ['+str(len(reference_filenames))+'] reference files for testing.')
  print('  Located ['+str(len(evaluation_filenames))+'] evaluation files for testing.')
  
  ref_hash_proc_pool = multiprocessing.Pool(processes=args.jobs)
  ref_hash_list = ref_hash_proc_pool.map(hash_file_to_hex_str, reference_filenames)
  ref_hash_proc_pool.close()
  print('  Collected ['+str(len(ref_hash_list))+'] hashes for files in the reference directory.')
  
  eval_proc_pool = multiprocessing.Pool(processes=args.jobs)
  partial_func_job = partial(_get_file_unrepresented_in_archive, ref_hash_list)
  unrepresented_file_list = eval_proc_pool.map(partial_func_job, evaluation_filenames)
  eval_proc_pool.close()
  
  print()
  print('Found following unrepresented files:')
  for filename in unrepresented_file_list:
    if filename: print('    '+filename)
  
def _build_argument_parser():
  ROOT_PARSER_DESC = 'File utility tool suite.'
  SUB_PARSER_HELP = 'sub-command help'
  REPORT_ARG_HELP = 'Output the report to a file.'
  JOBS_ARG_HELP = 'Number of job processes to run.'
  REPR_PARSER_HELP = ('Check if copies of the files in a evaluation directory '
                      'are present in a reference directory.')
  REPR_ARG_REF_HELP = 'The directory containing the files to confirm against.'
  REPR_ARG_EVAL_HELP = ('The directory containing the files to search for in '
                        'the reference directory.')
  DUPL_PARSER_HELP = 'Check for duplicate files in a directory.'
  DUPL_ARG_DIR_HELP = 'The directory containg the files to evaluate.'
  EVAC_PARSER_HELP = 'Monitor a directory, and evacuate the contents when files become available.'
  EVAC_ARG_MON_HELP = 'The directory to monitor.'
  EVAC_ARG_DEST_HELP = 'The destination to copy the files too.'

  import argparse
  parser = argparse.ArgumentParser(description=ROOT_PARSER_DESC)
  parser.set_defaults(func=None)
  subparsers = parser.add_subparsers(help=SUB_PARSER_HELP)
  
  repr_parser = subparsers.add_parser('repr', help=REPR_PARSER_HELP)
  repr_parser.add_argument('refdir', help=REPR_ARG_REF_HELP)
  repr_parser.add_argument('evaldir', help=REPR_ARG_EVAL_HELP)
  repr_parser.add_argument('--report', help=REPORT_ARG_HELP)
  repr_parser.add_argument('--jobs', help=JOBS_ARG_HELP, type=int, default=1)
  repr_parser.set_defaults(func=_repr_main)
  
  dupl_parser = subparsers.add_parser('dupl', help=DUPL_PARSER_HELP)
  dupl_parser.add_argument('dir', help=DUPL_ARG_DIR_HELP)
  dupl_parser.add_argument('--report', help=REPORT_ARG_HELP)
  dupl_parser.add_argument('--jobs', help=JOBS_ARG_HELP, type=int, default=1)
  dupl_parser.set_defaults(func=_dupl_main)
  
  evac_parser = subparsers.add_parser('evac', help=EVAC_PARSER_HELP)
  evac_parser.add_argument('mondir', help=EVAC_ARG_MON_HELP)
  evac_parser.add_argument('dest', help=EVAC_ARG_DEST_HELP)
  evac_parser.set_defaults(func=_evac_main)
  
  return parser
  
if __name__ == '__main__':
  parser = _build_argument_parser()
  args = parser.parse_args()
  
  if args.func:
    args.func(args)
  else:
    parser.print_help()
  