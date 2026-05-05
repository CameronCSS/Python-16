from collections import Counter, defaultdict, namedtuple, deque

numbers = [8,9,7,5,6,8,34,5,6,9,5,7,5,4,8,0,3,33,8]

# Count how many times each repeated
print(Counter(numbers))

# also works for words or letters
print(Counter('mississippi'))

sentence = 'you will remember me tomorrow if you remember anything'
print(Counter(sentence.split()))

# you can also use Counter methods to get data out
series = Counter([1,1,2,4,5,6,1,6,6,7,8,3,4,6,1,1,1,6,7,8])
print(series.most_common())

# regular dictionary
my_dict = {1 : 'green', 2 : 'blue', 3 : 'red'}
# throws key error when trying to find key that doesnt exist
try:
    print(my_dict[4])
except KeyError:
    print("That key doesnt exist")

# we can instead use defaultdict
new_dict = defaultdict(lambda: 'nothing')
new_dict[1] = 'green'
print(new_dict[2])
# This also assigns the lambda definition to that value you just tried to look up
# you can see the 'nothing' key is now in our dict
print(new_dict)

# with a normal tuple. you can easily lookup a value
# this will return the expected value

my_tuple = (500, 800, 65)
print(my_tuple[1])

# You can use tuples more like a dictionary by using a namedtuple
person = namedtuple('person', ['name', 'height', 'weight'])
# then assign attributes
michael = person('Michael', 1.76, 79)

# and now you can lookup those attributes.
print(michael.height)

# deque is a double linked list. which you can add to or pop from either left OR right. Unlike a normal list
# for example
my_list = deque(['first', 'second', 'third'])
my_list.appendleft('zero')
print(list(my_list))

# you can also use reverse
my_list.reverse()
print(list(my_list))

# or build a bad version of a reverse
# first create list to build
reversed_list = deque()

for item in my_list:
    reversed_list.appendleft(item)
print(list(reversed_list))

# you can even shift elements in a deque
# we can use this to build a really terrible reverse
count = 0
for item in my_list:
    count += 1
my_list.rotate(count)
print(list(my_list))