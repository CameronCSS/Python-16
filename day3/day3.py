"""
Day 3 was all about lists, dictionaries, tuples, and sets. and all the advanced features you can do with them
Like pop, append, extend. lists and dictionaries INSIDE of other lists and dictionaries.
dict.keys(), dict.values() and dict.items()

dict.values() will give you JUST the values
Example:
for value in dic.values():
    print(value)
    
for the pair of key AND value, use dict.items()
Example:
for key, value in dic.items():
    print(key, value)
    
tuples are like lists. exept they are immutable. tuples take less memory and are faster than lists

set is like dict. but each item can only be ONCE. Set will automatically dump duplicates. Sets are NOT indexed.
Sets cannot have lists or dictionaries. You CAN use tuples
The set keyword will only take one argument. so you must enclose elements with brackets or parenth.

You can also just create a set with curly braces, but unlike dict there are no pairs so python knows its a set
"""

# dic = {'k1' : ['a', 'b', 'c'], 'k2':['d', 'e', 'f']}
# dic['k3'] = ['g', 'h', 'i']
# word = []

# for key, letters in dic.items():
#     upper = [letter.upper() for letter in letters]
#     dic[key] = upper
#     word.extend(upper)
    
# print("".join(word))
# print(dic)

# tuple1 = (1,2,3,1)

# # Count will show how many of that item
# print(tuple1.count(1))

# # Index will give index of that item, but only the first found index.
# print(tuple1.index(1))


# my_set_1 = {1, 2, "three", "four"}

# my_set_2 = {"three", 4, 5} 

# my_set_3 = my_set_1.union(my_set_2)

"""-----------------------------------------"""

"""------ DAY 3 CHALLENGE ------"""

#  TEXT PARSER

# Take Text input from user
user_text = input("Enter some text: ").lower()

# debug print
# print(user_text)

# Ask user to enter 3 random letters
rand_letters = []

# Check if user entered JUST a letter
# Not checking if int. int is ok I guess

choices_dict = {3 : "first", 2: "second", 1: "third"}

i = 3
while i != 0:
    new_letter = input(f"Enter the {choices_dict[i]} letter: ")
    if len(new_letter) > 1:
        print("Please enter JUST a letter")
        continue
    elif len(new_letter)== 0:
        print("Please enter a letter")
        continue
    else:
        rand_letters.append(new_letter.lower())
        i -= 1
    
    
# debug print
# print(rand_letters)

print("\n*******************************\n")
input("\nPress Enter to process your results...")
print("\n*******************************\n")

# 1. How many times each of those letters appear (count upper and lower)
# Store in list and check how many times substring appears in string?
found_dict = {}

for letter in rand_letters:
    if letter in user_text:
        count = user_text.count(letter)
        found_dict[letter] = count
    else:
        found_dict[letter] = 0


letter_counts = (", ".join(f"[{key}] {value} times" for key,value in found_dict.items()))
    
print("\n****LETTERS REPEATED RESULTS****\n")
print(f"Found {letter_counts} in your text")
print("\n*******************************\n")
input("\nPress Enter to continue...")

# 2. How many words are in the text?
# use function to transform original text to a list, then check length
text_list = list(user_text.split())

print("\n****WORD COUNT****\n")
print(f"Your text was {len(text_list)} words long")
print("\n*******************************\n")
input("\nPress Enter to continue...")

# 3. First and last letters of the entered text
first = user_text[0][0]
last = user_text[-1][-1]

print("\n****FIRST AND LAST LETTERS****\n")
print(f"First letter: {first}")
print(f"Last letter: {last}")
print("\n*******************************\n")
input("\nPress Enter to continue...")

# 4. What would text look like in reverse?
text_list.reverse()

print("\n****REVERSED TEXT****\n")
print("This is your text in reverse: \n")
print(" ".join(text_list))
print("\n*******************************\n")
input("\nPress Enter to continue...")

# 5. is 'python' in the text
# Use bool to check, use dictionary to associate bool with answer
has_python = False

had_python_dict = {True : "had", False : "did not have"}

if "python" in user_text:
    has_python = True
    
print("\n****CONTAINED PYTHON??****\n")
print(f"\n The text you entered {had_python_dict[has_python]} python in it.")
print("\n*******************************\n")