import re
import os
import sys

def invert_single_assertion(file_string,match,replacement):
  """Invert an assertion by replacing the old one, using the regex match"""

  repl_string = 'assert(' + match.group(1) + replacement + match.group(3) + ')'
  result = file_string[:match.start()] + repl_string + file_string[match.end():]
  return re.sub('@expect verified', '@expect error', result)

def fail_suffix(i):
  """Filename suffix for the ith failing file"""
  if i == 0:
    return '_fail'
  else:
    return '_fail_' + str(i+1)

def fail_filename(orig_filename,i):
  """Filename for a failing regression"""
  parts = orig_filename.split('.')
  parts[-2] += fail_suffix(i)
  return '.'.join(parts)

def invert_assertions(filename,original="==",replacement="!="):
  """Inverts each assertion in a file, writing each one seperately to a new file."""

  orig_file = ""
  with open(filename, "r") as f:
    orig_file = f.read()
  
  regex = r'assert\((.*)(' + original + r')(.*)\)'
  matches = re.finditer(regex,orig_file)

  i = 0
  for match in matches:
    new_file_str = invert_single_assertion(orig_file,match,replacement)

    with open(fail_filename(filename,i), "w") as f:
      f.write(new_file_str)

    i += 1

def main():
  reg_list = [
      'hello',
      'compute',
      'function',
      'forloop',
      'fib',
      'compound',
      'array',
      'pointer',
      'method',
      'dynamic',
      'inout',
      'overload',
      ]
  folder = sys.argv[1]
  os.chdir(folder)
  for src_file in os.listdir('.'): # current directory, which we just changed into
    parts = src_file.split('.')
    reg_name = parts[-2]
    if reg_name in reg_list:

      if parts[-1] in ['f', 'f90', 'f95', 'for', 'f03']:
        invert_assertions(src_file,"==","/=")
        continue 
      # just do FORTRAN hello world manually, not worth the effort
      if parts[-2] == 'hello':
        invert_assertions(src_file,"true","false")
      else:
        invert_assertions(src_file)

if __name__ == '__main__':
  main()
