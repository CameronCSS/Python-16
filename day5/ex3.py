def double_zero(*args):
    
    for index, number in enumerate(args):
        if args[index + 1] == len(args):
            return False
        elif number == 0 and args[index + 1] == 0:
                return True
    return False

print(double_zero(0,1,5,1,0,9,3,5,0))