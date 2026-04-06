"""
All my helper functions to run my main code are in here.
I prefer to do this to keep the main py clean.
Only needing to dig deeper when things dont work
"""

def print_header(version):
    print(f"\n-----{version}-----\n")

def print_names(names):
    for name in names:
        print(f"Hello {name.title()}")