import re

# --- Setup ---------------------------------------------------------


text = 'If you need help call (658)-598-9977 any time for online help'

pattern = 'help'

search = re.search(pattern, text)
# can print the full re object to get all details
print(search)

# or can just print span to get the start and end of the match
print(search.span())

# You can use findall to find all occurences of that pattern
find_all = re.findall(pattern, text)
# use len to find how many times it was found
print(len(find_all))

# or we can print all of them by using a loop
print(f'Found [{pattern}] at: ')
count = 0
for found in re.finditer(pattern, text):
    print(f'{found.span()}')
    count += 1
    if len(find_all) > 1 and count < len(find_all):
        print('and at ')
        
new_text = 'call 564-526-6288 right now!!'

pattern = r'(\d{3})-(\d{3})-(\d{4})'

is_tele = re.search(pattern, new_text)
if is_tele is not None:
    print(f'\nPhone Number found at: {is_tele.span()}\n')
else:
    print('No Phone number found.')
    
groups = ['first', 'second', 'third']
for index, group in enumerate(groups, 1):
    print(f'{group} group of numbers: [{is_tele.group(index)}]')
    

# --- Password Check ---------------------------------------------------------

while True:
    password = input("Password: ")

    # This only checks if the password does NOT start with a number
    # AND that it is 8 characters long
    pattern = r'\D{1}\w{7}'
    
    check = re.search(pattern, password)
    
    if check is not None:
        print('Password Accepted')
        break
    else:
        print('Invalid Password. Try again!')

# --- Search for words ---------------------------------------------------------

some_text = 'The restaraunt is closed saturday and sunday.'


days_to_check = ['sunday', 'monday']

pattern = fr'({days_to_check[0]}|{days_to_check[1]})'

match_day = re.search(pattern, some_text, re.IGNORECASE) 

if match_day:
    day_found = match_day.group(1).lower()
    
    if day_found == days_to_check[0]:
        print(f'\nRestaraunt is closed {days_to_check[0]}')
    elif day_found == days_to_check[1]:
        print(f'\nRestaraunt is closed {days_to_check[1]}')
    else:
        print('\nRestaraunt is not closed on those days')

# --- Check Email ---------------------------------------------------------
