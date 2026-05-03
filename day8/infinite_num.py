def practice_generator():
    x = 1
    while True:
        yield x 
        x += 1 

inf_num = practice_generator()

print(next(inf_num))
print(next(inf_num))
print(next(inf_num))



def my_generator():
    x = 7
    while True:
        yield x
        x = x * 7
    
practice_generator = my_generator()

def reduce_lives():
    lives = 3
    while lives > 0:
        word = 'lives'
        if lives == 1:
            word = 'life'
        yield f"You have {lives} {word} left"
        lives -= 1
    else:
       yield f"Game Over" 

lose_live = reduce_lives()

print(next(lose_live))
print(next(lose_live))
print(next(lose_live))
print(next(lose_live))