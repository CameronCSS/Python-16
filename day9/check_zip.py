"""
This basic function checks if entered code is a zipcode or not

Args:
    zipcode: User entered text that is verified to be a zipcode or not.

Returns:
    Print success or failure
"""
# --- Imports ---------------------------------------------------------
import re

def main():
    """
    takes user input and checks if it is a zip based on defined criteria
    
    Args:
        zipcode: user input that is checked against criteria.
    
    Returns:
        Printout true or false
    """
    while True:
        zipcode = input('Enter a zipcode: ')

        # Basic check to see if all entered are digits AND only 5 long
        check = re.search(r'^\d{5}$', zipcode)
        if check is not None:
            print(f'[{zipcode}] is a Zipcode')
        else:
            print(f'[{zipcode}] is NOT a zipcode')

        again = input('Want to check another? (y/n)')

        if again == 'n':
            break

    print("Thanks for using the zipcode checker!")

if __name__ == "__main__":
    main()
