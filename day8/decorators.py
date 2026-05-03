def change_letters(type):
    """
    Returns the chosen function
    """
    
    def uppercase(text):
        print(text.upper())
        
    def lowercase(text):
        print(text.upper())
        
    if type == 'up':
        return uppercase
    elif type == 'low':
        return lowercase
    else:
        return 'Error'

operation = change_letters('up')

operation('word')