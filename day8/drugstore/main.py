"""
This program is a ticketing system that assigns a ticket number to customer 
the ticket number is based on which department they select
"""

from numbers import give_number, ticket_generator

# Each will use its own generator

# Perfumes = P -
# Medicine = M -
# Cosmetics = C -

# Use decorator to apply "Your number is: " to the return
# Use same decorator, or different one to append
# "Please Wait... someone will be with you shortly."

options = ['perfumes', 'medicine', 'Cosmetics']

def menu():
    """
    This function is the menu. it takes user input.
    Input is verified to work with given options.
    """

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

    # Previously had 3 generator codes
    # We dont need separate generator codes.
    # THESE count as separate generators by declaration
    perf_tickets = give_number(ticket_generator('P'))
    med_tickets = give_number(ticket_generator('M'))
    cosm_tickets = give_number(ticket_generator('C'))

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
                print("\n--- Thank you. Have a good day ---\n")
                break



if __name__ == "__main__":
    main()
