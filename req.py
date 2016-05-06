import os
import sys
from subprocess import call
cmd = os.path.join(sys.prefix, 'bin', 'pip')
print("1. Create a file called requirements.txt: File -> New... -> File")
print("2. Copy the output between the lines (---'s) below into the file")
print('-' * 20)
call([cmd, "freeze"])
print('-' * 20)
print('Copy the output above between the lines (---\'s) into a new file called requirements.txt')