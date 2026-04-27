from pathlib import Path
import os

cwd = os.getcwd()

def open_read(file):
    file_path = Path(cwd, file)
    
    file = open(file_path, 'r')
    
    return file.read()
    
    
print(open_read("example.txt"))


import os 
from pathlib import Path 

cwd = os.getcwd()

def overwrite(filename):
    file_path = Path(cwd, filename)
    
    file = open(file_path, 'w')
    
    file.write("content deleted")
    
    file.close()
    
    file = open(file_path, 'r')

    return file.read()
    
    
print(overwrite("example.txt"))