import os

def get_cwd():
    cwd = os.getcwd()
    
    return cwd

def clear_screen():
    # 'nt' means Windows, others cover Linux, Mac, etc.
    os.system('cls' if os.name == 'nt' else 'clear')

def space_blank():
    # print basic spacer
    print()
    
def spacer():
    # print basic spacer
    print("__________________________________________")
    
    
def welcome():
    # print basic spacer
    print("Welcome to the great Python Recipe book!!")
    
    
def goodbye():
    # print basic spacer
    print("Thank you for using the Python Recipe book!")