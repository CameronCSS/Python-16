def unique_items():
    '''
    This function finds all the unique items in the list,
    and returns them in the original order
    '''
    # Cant use set because we need to keep original order
    items = [1,2,3,4,5,5,3,6,1,4,7]
    
    # verbose
    unique_items = []
    for item in items:
        if item not in unique_items:
            unique_items.append(item)
    print(unique_items)
    
    # quick 1 liner
    print(list(dict.fromkeys(items)))
    

    
def most_expensive(products):
    highest = 0
    most = ''
    for item, price in products:
        if price > highest:
            highest = price
            most = item
    return most

def most_one_liner(products):
    return max(products, key=lambda item: item[1])[0]

products = ('coffee', 1.5), ('laptop', 500), ('muffin', 2.5), ('marshmallow', 1)
            

def check_3_digits(number):
    return number in range(100, 1000)

def show_3_digits(numbers):
    return [n for n in numbers if n in range(100, 1000)]

def one_3_digits(numbers):
    return any(n in range(100,1000) for n in numbers)

def all_3_digits(numbers):
    return all(n in range(100, 1000) for n in numbers)


    
if __name__ == "__main__":
    numbers = [145,675,76,789]
    unique_items()
    print(show_3_digits(numbers))
    print(one_3_digits(numbers))
    print(all_3_digits(numbers))