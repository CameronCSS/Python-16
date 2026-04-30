class Animal:
    
    def __init__(self, age, color):
        self.age = age
        self.color = color
    
    def born(self):
        print("This animal has been born")

    def talk(self):
        print("This animal makes a sound")

class Bird(Animal):
    
    def __init__(self, age, color, altitude):
        super().__init__(age, color)
        self.altitude = altitude
    
    def talk(self):
        print("chirp")
        
    def fly(self):
        print(f"This bird flies at {self.altitude} feet")
    


tweeter = Bird(5, 'yellow', 150)

tweeter.born()

tweeter.talk()

tweeter.fly()