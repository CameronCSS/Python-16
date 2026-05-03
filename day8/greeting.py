def decorate_greeting(function):
    
    def another_function(word):
        
        print('Hello')
        function(word)
        print('Goodbye')
        
    return another_function

def uppercase(text):
    print(text.upper())
    
def lowercase(text):
    print(text.lower())

greet_uppercase = decorate_greeting(uppercase)

uppercase('Python')

greet_uppercase('Python')

    
