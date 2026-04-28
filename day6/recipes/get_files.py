from pathlib import Path
from helpers import get_cwd, space_blank, clear_screen
from file_manager import delete_category

cwd = get_cwd()

def find_recipe(category):
    # base path, with specifically .txt files
    folder = Path(cwd).glob(f'{category}/*.txt')
    
    # all files path grabbed
    recipes_files = [file for file in folder]
    
    recipes = [rec.stem for rec in recipes_files]
    
    return pick_recipe(recipes)

def get_recipes():
    # base path, with specifically .txt files
    folder = Path(cwd).glob(f'**/*.txt')
    
    # all files path grabbed
    recipes_files = [file for file in folder]
    
    recipes = [rec.stem for rec in recipes_files]
    
    return recipes

def get_categories():
    # base path
    folder = Path(cwd)
    # get all folders inside
    category_folders = [file for file in folder.iterdir() if file.is_dir()]
    
    # List of all folders
    categories = [cat.stem for cat in category_folders]
    
    return categories
    
def count_recipes():
    return len(get_recipes())

def count_categories():
    return len(get_categories())


def print_categories():
    categories = get_categories()
    while True:
        print("Categories: ")
        for index, category in enumerate(categories):
                if category == "__pycache__":
                    continue
                print(f"[{index+ 1 }] {category}")
        choice = input(f"Pick a category [1-{len(categories)-1}]")
        if not choice.isdigit():
            clear_screen()
            continue
        else:
            choice = int(choice)
            pass
        if choice in range(1, (len(categories))):
            delete_category(categories[choice - 1])
            break
        else:
            # Clear screen and prompt again
            clear_screen()
            continue
        
def pick_category():
    categories = get_categories()
    space_blank()
    while True:
        print("Categories: ")
        for index, category in enumerate(categories):
            if category == "__pycache__":
                continue
            print(f"[{index+ 1 }] {category}")
        space_blank()
        choice = input(f"Pick a category [1-{len(categories)-1}]")
        if not choice.isdigit():
            clear_screen()
            continue
        else:
            choice = int(choice)
            pass
        if choice in range(1, (len(categories))):
            return find_recipe(categories[choice - 1])
            break
        else:
            # Clear screen and prompt again
            clear_screen()
            continue
        
def pick_recipe(recipes):
    
    space_blank()
    while True:
        print("Recipes: ")
        for index, recipe in enumerate(recipes):
            print(f"[{index + 1 }] {recipe}")
        space_blank()
        choice = input(f"Pick a category [1-{len(recipes)}]: ")
        if not choice.isdigit():
            clear_screen()
            continue
        else:
            choice = int(choice)
            pass
        if choice in range(1, (len(recipe))):
            try:
                return recipes[choice - 1]
            except IndexError:
                clear_screen()
                continue
        else:
            # Clear screen and prompt again
            clear_screen()
            continue

def print_recipe(recipe_name):
    try:
        # find file
        # Use Next to look in path and see if file exists, otherwise return None
        file = next(Path().glob(f'**/{recipe_name}.txt'), None)
        if file:
            space_blank()
            print(file.read_text())
        else:
            print(f"{recipe_name} does not exist. Try again.")                
    
    # Throw file not found if cant find
    except Exception as e:
        print(f"Error occured: {e}")
        
    