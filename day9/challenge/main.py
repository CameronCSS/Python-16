import os
import re
import math
import time
from datetime import date

def main():
    """
    Searched through folder structure checking all txt files for defined serial number pattern
    N[3 text chars]-[5 digits]
    """
    cwd = os.getcwd()

    path = os.path.join(cwd, 'My_Big_Directory')

    pattern = r'N[a-zA-Z]{3}-\d{5}'

    results = []

    start = time.time()

    for folders, subfolders, files in os.walk(path):
        subfolders[:] = [sub for sub in subfolders if sub not in ('.git', '__pycache__')]
        for file in files:
            # full path to the file
            filepath = os.path.join(folders, file)
            with open(filepath, 'r') as f:
                # read the entire file
                content = f.read()
            # search for the pattern
            match = re.search(pattern, content)
            if match:
                # store the result
                results.append((file, match.group()))
    end = time.time()
    duration = math.ceil(end - start)

    print(f"Search date: {date.today().strftime('%d/%m/%y')}")

    print("FILE\t\tSERIAL NO.")
    print("----\t\t----------")
    for file, serial in results:
        print(f"{file}\t{serial}")
    print(f"\nNumbers found: {len(results)}")
    print(f"Search duration: {duration} seconds")

if __name__ == "__main__":
    main()
