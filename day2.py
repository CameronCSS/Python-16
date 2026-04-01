name = input("What is your name? ")
sales = float(input("How much did you sell? "))

commish = round(((sales * 13) / 100), 2)

print(f"{name} has earned ${commish} in commision")