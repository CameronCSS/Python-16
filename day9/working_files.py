import os
import shutil
from send2trash import send2trash

cwd = os.getcwd()

print(cwd)

file = open('course.txt', 'w')
file.write('test text')
file.close()

new_path = f'{cwd}\\texts\\course.txt'

try:
    shutil.move('course.txt', new_path)
except FileNotFoundError:
     os.makedirs(f'{cwd}\\texts\\')
     print("Directory didnt exist. Created directory. Will try moving again")
finally:
    shutil.move('course.txt', new_path)
    print(f'successfully moved to {new_path}')

print('Now that we know its been created. Lets send it to the trash')

# send2trash is the safe way to delete. shutil delete permanently deletes file and it is not recoverable.
try:
    send2trash(new_path)
    os.rmdir(f'{cwd}\\texts\\')
except:
    print("Error occured. File not sent to trash.")


path = 'C:\\Users\\csseamons\\Desktop\\Python\\Python-16'

for folders, subfolders, files in os.walk(path):
    # This line modifies list in place and ignores .git and pycache folders in our printout
    subfolders[:] = [sub for sub in subfolders if sub not in ('.git', '__pycache__')]

    # We can add a file filter here to ONLY find desire files and print its tree path
    if not any(file.startswith('main') for file in files):
        continue

    print(f'In folder: {folders}')
    if subfolders:
        print(f'Subfolders are: ')
        for sub in subfolders:
            if sub:
                print(f'\t{sub}')
    if files:
        print('Files are: ')
        for file in files:
            print(f'\t{file}')
    print('\t')