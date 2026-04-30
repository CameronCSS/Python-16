import os


cwd = os.getcwd()

path = f"{cwd}\\test.txt"

print(path)

file = open(path, 'a+')

new_lines = ['Hello', 'world', 'here', 'I am']

for line in new_lines:
    file.writelines('\n' + line)

file.seek(0)

for line in file:
        print(line.strip())

file.close()