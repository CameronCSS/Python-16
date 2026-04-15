# Interactions Between Functions Practice #2

"""
Create a function called reduce_list() that takes a list (numbers) as an argument,
 and returns also a list, but removing duplicates 
 (leaving only one of the numbers if there are duplicates) 
 and removing the highest value. The order of the elements can be changed.

For example, if given the list [1,2,15,7,2] it should return [1,2,7].

Create a function called average() that can receive as an argument 
the list returned by the previous function, 
and that calculates the average of its values. 
It should return the result (a float), without printing it.
"""


numbers = [1,2,15,7,2]


def reduce_list(numbers):
    new_list = []
    # remove duplicates
    for num in numbers:
        if num not in new_list:
            new_list.append(num)
    
    max_num = max(new_list)
    for index, num in enumerate(new_list):
        if num == max_num:
            new_list.pop(index)
    return new_list
        

def average(num_list):
    list_sum = sum(num_list)
    list_length = len(num_list)
    
    return list_sum / list_length