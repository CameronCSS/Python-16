def sum_up(*args):
    return sum(num for num in args)


def sum_squares(*args):
    
    return sum(num ** num for num in args)

print(sum_squares(1,2,3))