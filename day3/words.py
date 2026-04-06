""" Separated funcitons to have a cleaner main.py"""


# Split the text into a list of words
def word_count(words):
    word_count = len(words)
    # Print the count
    return word_count

def reverse_the_words(words):
    reversed_words = words.copy()
    reversed_words.reverse()
    reversed = " ".join(reversed_words)
    
    return reversed

def find_python(words):
    python_count = words.count("python")
    if python_count > 0:
        return f"Your text had Python in it [{python_count}] times."
    else:
        return f"Your text did not have Python in it"

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

    return round(sum(len(word) for word in words) / len(words),2)
    
def title_case(words):
    # Print what the text would look like in Title Case
    # Do NOT use the built in title() method - try to do it manually
    upper_words = []
    
    # Geting reverse since we are appending from the end
    for word in words:
        new_word = word[0].upper() + word[1:]
        upper_words.append(new_word)
    
    new_words = " ".join(upper_words)
    
    return new_words


def highest(words):
    high_word, high_count = most_common(words)
    if high_count == 1:
        return "All words were unique, and only in your text 1 time."
    else:
        return f"The most common word [{high_word}] was in your text [{high_count}] times."