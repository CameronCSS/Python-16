import os

cwd = os.getcwd()

path = f'{cwd}\My_Big_Directory'

for folders, subfolders, files in os.walk(path):
    # This line modifies list in place and ignores .git and pycache folders in our printout
    subfolders[:] = [sub for sub in subfolders if sub not in ('.git', '__pycache__')]

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