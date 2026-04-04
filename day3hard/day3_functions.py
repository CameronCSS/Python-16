""" Separated funcitons to have a cleaner main.py"""
# All helper functions needed for day3 program


import os

def get_text():
    user_text = input("Enter some text: ").strip().lower()
    cleaned_text = "".join(char for char in user_text if char.isalnum() or char.isspace())
    
    return cleaned_text

def spacer():
    # Need to give printout some space
    
    return "\n\n--------------------------------------\n\n"

def header():
    # Need to give a little header
    
    return "--------------------------------------"

def to_continue():
    # Need to take enter to continue
    # Do I need this as its own function??
    # possibly build more options, like start over?
    output = input("Press [Enter] to contnue.....")
    
    return

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    return


def section_break():
    print(spacer())
    to_continue()
    clear()