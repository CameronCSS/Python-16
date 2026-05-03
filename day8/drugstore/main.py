"""
This program is a ticketing system that assigns a ticket number to customer 
the ticket number is based on which department they select
"""

from numbers import perf_tickets, med_tickets, cosm_tickets

# Each will use its own generator

# Perfumes = P -
# Medicine = M -
# Cosmetics = C -

# Use decorator to apply "Your number is: " to the return
# Use same decorator, or different one to append
# "Please Wait... someone will be with you shortly."

def welcome():
    """
    Simple function to welcome the user
    """

    print('*' * 40)
    print(" --- Welcome to the Python drugstore ---")
    print('*' * 40)
    print()

def menu():
    """
    This function is the menu. it takes user input.
    Input is verified to work with given options.
    """

    options = ['perfumes', 'medicine', 'Cosmetics']

    while True:
        for x, option in enumerate(options, 1):
            print(f"[{x}] {option.title()}")
        choice = input("Make a selection: (q to quit) ")
        try:
            if choice == 'q':
                return choice
            choice = int(choice)
            if choice in range(1, len(options) + 1):
                return choice
        except ValueError:
            print("Please enter a valid number!")
            continue

def main():
    """
    This main function calls the menu and gets user input.
    Menu continues until user quits.
    """

    welcome()

    while True:
        choice = menu()
        match choice:
            case 1:
                print()
                perf_tickets()
                continue
            case 2:
                print()
                med_tickets()
                continue
            case 3:
                print()
                cosm_tickets()
                continue
            case 'q':
                break
        try:
            another = input("Do you need another ticket? y/n").lower()
        except ValueError:
            print('Please enter [y] or [n]')
        else:
            if another == 'y':
                continue

    print("\n--- Thank you. Have a good day ---\n")


if __name__ == "__main__":
    main()
