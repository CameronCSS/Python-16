"""---------------------------------"""
"""-------- DAY 3 CHALLENGE --------"""

from letters import *
from words import *
from day3_functions import *

#  TEXT PARSER

def main():
    # Take Text input from user
    user_text = get_text()
    words = user_text.split()

    section_break()

    # Ask user to enter 3 random letters
    letters = letter_list()

    section_break()


    # 1. How many times each of those letters appear
    print(header())
    print("Letter counts: ")
    print(f"Found {letter_count(letters, user_text)}")

    section_break()


    # 2. How many words are in the text?
    print(header())
    print("Word counts: ")
    print(f"Your text had [{word_count(words)}] words")

    section_break()


    # 3. First and last LETTERS of the entered text
    first, last = first_last(user_text)
    print(header())
    print(f"First letter in your text was [{first}]")
    print(f"Last letter in your text was [{last}]")

    section_break()


    # 4. What would the text look like in reverse?
    print(header())
    print("Your text reversed would look like: ")
    print(f"\n{reverse(words)}")

    section_break()


    # 5. Is 'python' in the text?
    print(header())
    print(find_python(words))

    section_break()


    # --- BONUS CHALLENGES ---

    # 6. What is the most common WORD in the text?
    high_word, high_count = most_common(words)
    print(header())
    if high_count == 1:
        print("All words were unique, and only in your text 1 time.")
    else:
        print(f"The most common word [{high_word}] was in your text [{high_count}] times.")

    section_break()


    # 7. How many unique words are in the text?
    print(header())
    print(f"There were [{unique_words(words)}] unique words in your text.")

    section_break()


    # 8. What is the average word length?
    print(header())
    print(f"The average length of words in your text was {avg_length(words)}")

    section_break()


    # 9. Vowel counter
    print(header())
    print("Vowel Counts: ")
    print(vowel_count(words))

    section_break()


    # 10. Title case the text
    title_case_text = " ".join(title_case(words))
    print(header())
    print("Your text in title case: ")
    print(f"\n {title_case_text} ")
    print("\n --- THANK YOU FOR USING MY TEXT PARSER --- \n")
    
if __name__ == "__main__":
    main()