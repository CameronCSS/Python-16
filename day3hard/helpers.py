""" Separated funcitons to have a cleaner main.py"""
# All helper functions needed for day3 program

# CLEAR function works best in Command prompt environment. Not in powershell

import os

def get_text():
    clear()
    user_text = input("Enter some text: ").strip().lower()
    cleaned_text = "".join(char for char in user_text if char.isalnum() or char.isspace())
    
    return cleaned_text

def spacer():
    # Need to give printout some space
    
    return "\n\n--------------------------------------\n\n"

def welcome():
    # Need to give printout some space
    clear()
    return print("\n\n------WELCOME TO THE TEXT PARSER 3000------\n\n")

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
    header()
    

def menu(options):
    selected = []
    
    while True:
        clear()
        print("Select your options: ")
        for i, option in enumerate(options, 0):
            mark = "X" if i in selected else " "
            print(f"Option {i}: [{mark}] {option}")
        print("a for ALL Options")
        print("(e) to exit")
        choice = input("Enter option number: ").strip()
        
        # Validate choice
        if choice == "e":
            break
        elif choice == "a":
            if len(selected) == len(options):
                selected = []
            else:
                selected = [0,1,2,3,4,5,6,7,8,9]
        elif choice.isnumeric() and 0 <= int(choice) <= len(options) - 1:
            num = int(choice)
            if num in selected:
                selected.remove(num)  # toggle off if already selected
            else:
                selected.append(num)  # toggle on
        else:
            print("Invalid option")
        
    return selected