class Cow:
    
    def __init__(self, name):
        self.name = name
        
    def talk(self):
        print(self.name + ' moos')
        
class Sheep:
    
    def __init__(self, name):
        self.name = name
        
    def talk(self):
        print(self.name + ' bleats')
        
cow1 = Cow('Mandy')
sheep1 = Sheep('Cloud')

def animal_talks(animal):
    animal.talk()
    
animal_talks(cow1)
animal_talks(sheep1)


a_word = "polymorphism"
a_list = ["Classes", "OOP", "Polymorphism"]
a_tuple = (1, 2, 3, 80)

items = [a_word, a_list, a_tuple]

def iterator(list):
    print(len(list))

for item in items:
    iterator(item)
    
    
    