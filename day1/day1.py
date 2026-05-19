import random

def get_random():
    rand = random.choice(["Color", "Animal", "Sport", "Movie", "Superhero", "Food", "Car", "City", "Country", "Book"])
    return rand

brand_name = []

while len(brand_name) < 2:
    question = input(f"What is your favorite {get_random()}? ")
    brand_name.append(question)



print(f"\nBeer Brand: {' '.join(brand_name)}")