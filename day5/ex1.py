def return_distincts(*args):
    
    total = sum(num for num in args)
    smallest = min(args)
    largest = max(args)
    if total > 15:
        return largest
    elif total < 10:
        return smallest
    else:
        return next(num for num in args if num not in [smallest, largest])
    

print(return_distincts(5,1,6))