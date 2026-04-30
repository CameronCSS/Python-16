class Father:
    
    def talk(self):
        print('Hello')

class Mother:
    def laugh(self):
        print('ha ha')
        
    def talk(self):
        print('How are you?')

# Because Father was inherited first, that method takes priority
class Child(Father, Mother):
    pass


class Grandchild(Child):
    pass

my_grandchild = Grandchild()

my_grandchild.laugh()
my_grandchild.talk()