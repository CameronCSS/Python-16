from pathlib import Path
from helpers import get_cwd
import shutil

cwd = get_cwd()

## Initialize base recipe folder structure

# Create original recipe list here
# This list will build old folders if you call the two functions below
recipes = {
    "dessert": ["brownies", "cheese cake"],
    "meat":    ["grilled chicken", "pork chops"],
    "pasta":   ["baked spaghetti", "penne alla vodka"],
    "salad":   ["chef salad", "greek salad"]  
    }


def create_recipe_files(recipe_dict):

    for folder, items in recipe_dict.items():
        folder_path = Path(folder)
        folder_path.mkdir(parents=True, exist_ok=True)
        for item in items:
            file = folder_path / f"{item}.txt"
            file.write_text("")

    insert_recipes()
    
    
def insert_recipes():
    folder_path = list(Path(cwd).glob('**/*.txt'))
    for folder in folder_path:
        text = str(Path(folder.stem))
        text = text.replace("_", " ")
        line = f"This is the recipe for {text}"

        file = open(folder, 'w')

        file.write(line)

        file.close()
        
## End Base structure
    
def create_category(cat_name):
    try:
        # Create path obj
        cat_path = Path(cat_name)
        
        # Create folder
        cat_path.mkdir(parents=True, exist_ok=True)
        
        return True
    
    except Exception as e:
        print(f"Error occured: {e}")
        return False
    
def create_recipe(category, recipe_name, text):
    try:
        # Create file
        file = Path(category) / f"{recipe_name}.txt"
        
        # Write user given text
        file.write_text(f"{text}")
        
        return True
    
    except Exception as e:
        print(f"Error occured: {e}")
        return False
    
    
def delete_category(cat_name):
    try:
        cat_path = Path(cat_name)
        
        # Verify it even exists
        if cat_path.exists():
            verify = input(f"Are you sure you want to delete {cat_name}? (y/n)")
            if verify == "y":
                shutil.rmtree(cat_path)
                print(f"Succesfully removed {cat_name}")
                return True
            else:
                print("Cancelled Delete")
        else:
            print(f"{cat_name} does not exist. Try again.")
        

    
    except Exception as e:
        print(f"Error occured: {e}")
    return False
    
def delete_recipe(recipe_name):
    try:
        # find file
        # Use Next to look in path and see if file exists, otherwise return None
        file = next(Path().glob(f'**/{recipe_name}.txt'), None)
        if file:
            verify = input(f"Are you sure you want to delete {recipe_name}? (y/n)")
            if verify == "y":
                # Delete recipe if exists
                file.unlink()
                return True
            else:
                print("Cancelled Delete")
        else:
            print(f"{recipe_name} does not exist. Try again.")                
    
    # Throw file not found if cant find
    except Exception as e:
        print(f"Error occured: {e}")
        
    return False
    
# TEST CALLS
# create_category("Vegan")

# create_recipe("Vegan", "Vegan Pizza", "This is how you make a vegan pizza")

# delete_category("Vegan")

# delete_recipe("Vegan Pizza")