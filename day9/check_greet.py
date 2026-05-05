"""
Check if user greeted the program by saying 'hello'
"""
# --- Imports ---------------------------------------------------------
import re

# --- main function ---------------------------------------------------------
def main():
    """
    Basic check to see if input contains 'hello'
    
    Args:
        sentence: user input
    
    Returns:
        response based on if their input passes or not
    """
    # Take users input
    sentence = input('Enter a greeting: ').title()

    was_greeted = re.search(r'(^Hello)', sentence)

    if was_greeted is not None:
        print('Ok')
    else:
        print('Not ok')

# --- Run Main ---------------------------------------------------------
if __name__ == "__main__":
    main()
