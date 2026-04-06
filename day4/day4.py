from helpers import print_header, print_names

names = ['john', 'ann', 'chad', 'lee', 'mary',]

# (What is taught in the 16 days of python course)
print_header("Simple for loop")
for name in names:
        print(f"Hello {name.title()}")


# (Technically one line. but harder to decipher at first glance)
print_header("List comprehension")
print("\n".join(f"Hello {name.title()}" for name in names))


# wrapping in a function, call it with a single line
print_header("Using Functions")
print_names(names)


""" 
For now (I am still very much a Junior dev)
I prefer to use the funciton wrapper.
Obsure the function away in a helper file, or away from the code.
Use good naming conventions and call the whole thing with one line
"""
