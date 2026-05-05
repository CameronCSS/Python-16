"""
This is practice of basic re functions
"""

import re

def main():
    """
    Crude and really simple email verification using basic regex
    
    Args:
        email: User email to check
    
    Returns:
        prints if Email is valid or not
    """
    while True:
        try:
            email =input("Enter an email to check: ")

            symbol = re.search(r'[@]', email)

            dot_com = re.search(r'\.com$', email)

            if symbol is not None and dot_com is not None:
                print("Email is Valid")
            else:
                print('Email is invalid. Try again')
        except ValueError as e:
            print(f"An error occurred: {e}")
        again = input('Would you like to check another? (y/n)')
        if again == 'n':
            break
    print("Thanks for using the email checker!")

if __name__ == "__main__":
    main()
