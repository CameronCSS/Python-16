from get_files import pick_category, print_recipe, print_categories
from file_manager import create_recipe, create_category, delete_recipe, delete_category
from helpers import clear_screen, space_blank, spacer

# Define Menu options
options = ['Read Recipes', 'Create Recipe', 'Create Category', 'Delete Recipe', 'Delete Category', 'Quit']

def menu():
    while True:
        try:
            for index, option in enumerate(options):
                print(f"[{index + 1}] {option}")
            choice = input("Enter Selection [1-6]:")
            # Verify they put in a number
            # isdigit doesnt handle all cases. but good enough for this case
            if not choice.isdigit():
                # Clear screen and prompt again
                clear_screen()
                continue
            # convert string input to int
            else:
                choice = int(choice)
                pass
            # Verify they selected one of the options
            if choice in range(1, (len(options) + 1)):
                handle_option(choice)
            else:
                # Clear screen and prompt again
                clear_screen()
                continue
            
            if choice == 6:
                break
            else:
                continue
        except KeyboardInterrupt:
            print("\nExiting...")
            exit()
        

## Option MAP
# 1. read recipe
# 2. create recipe
# 3. create category
# 4. delete recipe
# 5. delete category
# 6. end program

def handle_option(choice):
    clear_screen()
    match choice:
        case 1: # 1. read recipe
            print_recipe(pick_category())
        case 2: # 2. create recipe
            recipe_cat = input("Enter Recipe Category: ")
            recipe_name = input("Enter a name for your recipe: ")
            recipe_text = input("Enter your recipe text: ")
            create_recipe(recipe_cat, recipe_name, recipe_text)
        case 3: # 3. create category
            cat_name = input("Enter a name for your recipe: ")
            create_category(cat_name)
        case 4: # 4. delete recipe
            delete_recipe(pick_category())
        case 5: # 5. delete category
            print_categories()
        case 6: # Exit
            print("Quitting...")
        case _: # The underscore is the default catch-all
            # This should not be reachable with above menu coding
            print("Unknown option. try again")
            
    space_blank()
    
    return choice