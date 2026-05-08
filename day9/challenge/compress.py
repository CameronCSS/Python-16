import zipfile
import os

cwd = os.getcwd()

with zipfile.ZipFile(cwd + '/Project+Day+9.zip', mode='r') as archive:
    # List the contents of the archive
    archive.printdir()
    # Extract all contents
    archive.extractall()

print(f"Unzipped contents of {cwd}/Project+Day+9.zip")
