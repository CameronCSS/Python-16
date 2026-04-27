from pathlib import Path
import os

cwd = os.getcwd()


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
    
    
recipes = {
    "dessert": ["brownies", "cheese_cake"],
    "meat":    ["grilled_chicken", "pork_chops"],
    "pasta":   ["baked_spaghetti", "penne_alla_vodka"],
    "salad":   ["chef_salad", "greek_salad"]  
    }


create_recipe_files(recipes)

# Welcome user

# Tell user where recipes are located

# Tell them how many recipes they have

# ----
# Give them options

# 1. read recipe
# 2. create recipe
# 3. create category
# 4. delete recipe
# 5. delete category
# 6. end program

## Secondary options

# # 1. read recipe
# 1. Choose category
# 2. show recipes
# 3. choose a recipe
# 4. shows that recipe

# # 2. create recipe
# 1. Choose category
# 2. create name
# 3. create content

# # 3. create category
# 1. category name
# 2. create new dir with that name

# # 4. delete recipe
# 1. Choose category
# 2. show recipes
# 3. choose a recipe
# 4. delete that recipe

# # 5. delete category
# 1. Choose category
# 2. delete category
