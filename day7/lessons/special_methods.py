# # special methods
# __init__
# __name__
# __mro__
# __bases__
# __subclasses__


class Object:
    
    def __init__(self, length):
        self.length = length
        
    def __len__(self):
        return self.length

my_object = Object(5)
print(len(my_object))


class CD:
    
    def __init__(self, songwriter, title, songs):
        self.songwriter = songwriter
        self.title = title
        self.songs = songs
        
    def __str__(self):
        return f'Album: {self.title} by {self.songwriter}'
    
    def __len__(self):
        return self.songs
    
    def __del__(self):
        print(f'Album [{self.title}] has been deleted')
        
my_cd = CD('Pink Floyd', 'The Wall', 24)
           
print(str(my_cd))
print(len(my_cd))

# This will delete the object
# We can define custom attributes to the built in function do display more info
del my_cd

