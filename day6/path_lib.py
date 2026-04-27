from pathlib import Path
import os

cwd = os.getcwd()

print(cwd)

folder = Path(cwd)

names = ['text', 'test', 'stress', 'next']

suffix = '.txt'

folders = [folder.with_name(f"{name}{suffix}") for name in names]

# There are a lof of methods to see file info.

# This gives full filename
print(", ".join(folder.name for folder in folders))

# This gives just the file name without the suffix
print(", ".join(folder.stem for folder in folders))

# This gives file type / suffix
print(", ".join(folder.suffix for folder in folders))

# You can also check if file exists with a method
for folder in folders:
    if not folder.exists():
        print(f"'{folder.name}' does not exist")
    else:
        print(f"'{folder.name}' exists")
     
#  Search cwd for .txt files   
for txt in Path(cwd).glob('**/*.txt'):
    print(txt)
