from helpers import get_cwd, clear_screen, spacer, space_blank, welcome, goodbye
from get_files import count_recipes
from menu import menu

cwd = get_cwd()

def main():
    
    # Welcome to the program
    clear_screen()
    welcome()
    space_blank()
    
    # Tell them how many recipes they have
    print(f"You have {count_recipes()} recipes")
    print(f"Recipes are located in {cwd}")
    space_blank()
    
    # Run menu
    menu()
    space_blank()
    
    # Say goodbye if they quit
    spacer()
    goodbye()
    spacer()
    
    
    
if __name__ == "__main__":
    main()