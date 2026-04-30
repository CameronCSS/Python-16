import os

def star_spacer():
    print('*' * 50)
    
def dub_spacer():
    print("\n\n")
    
def clear_screen():
    # 'nt' means Windows, others cover Linux, Mac, etc.
    os.system('cls' if os.name == 'nt' else 'clear')
    
def welcome():
    clear_screen()
    star_spacer()
    print("Welcome to Python Banking app!")
    star_spacer()