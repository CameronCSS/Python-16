def extract_letters(word):
    word_set = list(set(letter for letter in word))
    word_set.sort()
    
    return word_set

print(extract_letters("entertaining"))