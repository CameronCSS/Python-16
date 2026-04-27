import os

cwd = os.getcwd()

my_file = open(f"{cwd}/test.txt")

for line in my_file:
    print(line)



my_file.close()