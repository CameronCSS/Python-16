def unique_items():
    # Cant use set because we need to keep original order
    items = [1,2,3,4,5,5,3,6,1,4,7]
    
    # verbose
    unique_items = []
    for item in items:
        if item not in unique_items:
            unique_items.append(item)
    print(unique_items)
    
    # quick 1 liner
    print(list(dict.fromkeys(items)))
    
    
if __name__ == "__main__":
    unique_items()