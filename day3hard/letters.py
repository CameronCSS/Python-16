""" Separated funcitons to have a cleaner main.py"""

# Ask user to enter 3 random letters

def letter_list():
    letter_dict = {3: "first", 2: "second", 1: "third"}
    letters = []
    num = 3
    print("\nEnter letters to count in your text:")
    
    while num > 0:
        letter = input(f"Enter the {letter_dict[num]} letter: ").lower()

        # Validate: reject if a number
        if letter.isnumeric():
            print("Please enter a letter, not a number")
            continue
        # Validate: reject if more than 1 character
        elif len(letter) > 1:
            print("Please enter just ONE letter")
            continue
        # Validate: reject if empty
        elif len(letter) == 0:
            print("Please enter a letter")
            continue
        # Validate: reject if already in list
        elif letter in letters:
            print(f"Already used {letter}. Please enter a NEW letter")
            continue
        else:
            # store each valid letter
            letters.append(letter)
            num -= 1
    return letters

# 1. How many times each of those letters appear
def letter_count(user_text):
    letters = letter_list()
    
    # Store results
    letter_count = {}
    # If letter not found, store 0
    for letter in letters:
        letter_count[letter] = user_text.count(letter)

    # Print results in format: Found [e] 1 times, [t] 2 times in your text 
    letter_counts = ", ".join(f"[{letter}] {value} times" for letter,value in letter_count.items())
        
    return letter_counts

def vowel_count(words):
    # Count how many vowels (a, e, i, o, u) appear in the entire text
    full_text = " ".join(words)
    vowel_list = ["a", "e", "i", "o", "u"]
    vowel_dict = {v: full_text.count(v) for v in vowel_list if v in full_text}
        
    # Print results
    
    if len(vowel_dict) > 0:
        vowel_counts = ", ".join(f"[{vowel}] {value} times" for vowel,value in vowel_dict.items())
        results = f"Found {vowel_counts}"
    else:
        results = "No vowels in your text"
        
    return results

# 3. First and last LETTERS of the entered text
def first_last(user_text):
    # (not first word, but first character)
    first_letter = user_text[0][0]
    last_letter = user_text[-1][-1]
    
    return first_letter, last_letter

def show_first_last(user_text):
        first, last = first_last(user_text)
        print(f"First letter in your text was [{first}]")
        print(f"Last letter in your text was [{last}]")