import json
from pathlib import Path

DATA_DIR = Path(__file__).parent

#load a list of item in the file
def load(name):
    path = DATA_DIR / f"{name}.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)

#save an item into a path
def save(name, items):
    path = DATA_DIR / f"{name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

def next_id(items):
    return max((item["id"] for item in items), default=0) + 1

#getting an item
def get_one(name, item_id):
    for item in load(name):
        if item["id"] == item_id:
            return item
    return None

#create an item and save into a file
def create(name, new_item):
    items = load(name)
    item = {"id": next_id(items), **new_item}
    items.append(item)
    save(name, items)
    return item

#update an item with new data and return an old data
def update(name, item_id, new_data):
    items = load(name)
    for i, item in enumerate(items):
        if item["id"] == item_id:
            items[i] = {**item, **new_data, "id": item_id}
            save(name, items)
            return items[i]
    return None

#delete an item 
def delete(name, item_id):
    items = load(name)
    kept = [item for item in items if item["id"] != item_id]
    if len(kept) == len(items):
        return False
    save(name, kept)
    return True

#notice this
def delete_recipe(recipe_id):
    if not delete("recipes", recipe_id):
        return False
    entries = load("plan_entries")
    save("plan_entries", [e for e in entries if e["recipeId"] != recipe_id])
    return True
def delete_plan(plan_id: int) -> bool:
    if not delete("plans", plan_id):
        return False
    save("plan_entries", [e for e in load("plan_entries") if e["planId"] != plan_id])
    return True


def is_duplicate(plan_id, recipe_id, day, meal_type, ignore_id=None):
    for e in load("plan_entries"):
        if (e["id"] != ignore_id
                and e["planId"] == plan_id
                and e["recipeId"] == recipe_id
                and e["day"] == day
                and e["mealType"] == meal_type):
            return True
    return False

def entries_for(field, value):
    return [e for e in load("plan_entries") if e[field] == value]