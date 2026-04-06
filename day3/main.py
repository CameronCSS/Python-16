"""---------------------------------"""
"""-------- DAY 3 CHALLENGE --------"""

from letters import *
from words import *
from day4.helpers import *

# Add Parsing options as I add them
options = ["Letter count", "Word count", "First and Last", 
           "Reversed", "Find Python", "Most Common word", "Unique words", 
           "Average Length", "Vowel Count", "Title Case"]


#  TEXT PARSER

def main():
    welcome()
    to_continue()
    
    # Take Text input from user
    user_text = get_text()
    words = user_text.split()

    clear()
    
    # Build map of functions to call depending on options picked
    function_calls = {
    0: lambda: print(f"\nLetter counts: \nFound {letter_count(user_text)}"),
    1: lambda: print(f"Word counts: \nYour text had [{word_count(words)}] words"),
    2: lambda: show_first_last(user_text),
    3: lambda: print(f"Your text reversed would look like: \n{reverse_the_words(words)}"),
    4: lambda: print(find_python(words)),
    5: lambda: print(highest(words)),
    6: lambda: print(f"There were [{unique_words(words)}] unique words in your text."),
    7: lambda: print(f"The average length of words in your text was {avg_length(words)}"),
    8: lambda: print(f"Vowel Counts: \n{vowel_count(words)}"),
    9: lambda: print(f"Your text in title case: \n{title_case(words)} ")
    }
    
    # Call menu to get what options they select
    selected = menu(options)
    
    clear()
    
    print(f"You selected: ")    
    if len(selected) == len(options):
        print("All Options")
    else:
        print(f"{", ".join([options[num] for num in selected])} ")

    section_break()
    
    for num in selected:
        function_calls[num]()
        section_break()
        
    ans = input("Would you like to go again?? (y/n)").lower()
    if ans == "y":
        main()
    else:
        print("\n --- THANK YOU FOR USING MY TEXT PARSER --- \n")
    
if __name__ == "__main__":
    main()