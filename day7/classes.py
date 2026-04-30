class Bird:
    
    wings = True
    
    def __init__(self, color):
        self.color = color

    def flap(self):
        print("bird flaps wings...")
        print("flap")
        
    def chirp(self, count):
        for _ in range(0, count):
            print("Tweet")
        print(f"I am {self.color}")
        
    def paint_black(self):
        self.color = 'black'
        print(f"the bird is now {self.color}")
        
    @classmethod
    def _lay_eggs(cls, number):
        print(f'It laid {number} eggs')
    
    @staticmethod
    def look(direction):
        print(f"The bird looks {direction}")

my_bird = Bird('Blue')

new_bird = Bird('yellow')

my_bird.wings = False

my_bird.flap()

my_bird.chirp(4)

print(my_bird.wings)
print(new_bird.wings)

my_bird.look('west')