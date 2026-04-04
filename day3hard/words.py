""" Separated funcitons to have a cleaner main.py"""


# Split the text into a list of words
def word_count(words):
    word_count = len(words)
    # Print the count
    return word_count

def reverse(words):
    reverse_word = words
    reverse_word.reverse()
    reversed = " ".join(reverse_word)
    
    return reversed

def find_python(words):
    python = False
    had_python = {True : "had", False : "did not have"}
    if "python" in words:
        python = True
    
    python_count = 0
    for word in words:
        if word == "python":
            python_count += 1
    if python_count > 0:
        text = f"Your text {had_python[python]} Python in it [{python_count}] times."
    else:
        text = f"Your text {had_python[python]} Python in it"
    
    return text

def most_common(words):
    # Hint: you'll need to count occurrences of each word
    # Print the word and how many times it appeared
    word_counts = {}
    for word in words:
        word_counts[word] = words.count(word)
    
    highest_count = max(word_counts.values())
    for word, value in word_counts.items():
        if value == highest_count:
            highest_word = word
    
    return highest_word, highest_count


def unique_words(words):
    # Hint: think about a data type that removes duplicates automatically
    unique_words_set = set(words)
    
    unique_words_count = len(unique_words_set)
    
    return unique_words_count
    
def avg_length(words):
    # Loop through the word list, get each length, calculate the average
    lengths = []
    for word in words:
        lengths.append(len(word))
        
    avg_word_len = round(sum(lengths) / len(lengths),2)
    
    return avg_word_len
    
def title_case(words):
    # Print what the text would look like in Title Case
    # Do NOT use the built in title() method - try to do it manually
    upper_words = []
    for word in words:
        new_word = word[0].upper() + word[1:]
        
        upper_words.insert(0, new_word)
    
    return upper_words