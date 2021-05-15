import json
import utils

def show_list(user_id):
    utils.create_user(user_id)
    path = f"data/{user_id}/shopping.json"
    with open(path, "r") as f:
        current = json.load(f)
    if len(current) == 0:
        return "Your shopping list is empty."
    lines = ["Your shopping list:"] + [
        f"* {name}: {amt}"
        for name, amt in current.items()
    ]
    return "\n".join(lines)

def add(user_id, to_buy):
    utils.create_user(user_id)
    path = f"data/{user_id}/shopping.json"
    with open(path, "r") as f:
        current = json.load(f)
    for name, amt in to_buy.items():
        current[name] = current.get(name, 0) + amt
    with open(path, "w") as f:
        json.dump(current, f, indent=4)
    return show_list(user_id)

def remove(user_id, to_remove):
    utils.create_user(user_id)
    path = f"data/{user_id}/shopping.json"
    with open(path, "r") as f:
        current = json.load(f)
    for name in to_remove:
        current.pop(name, None)
    with open(path, "w") as f:
        json.dump(current, f, indent=4)
    return show_list(user_id) 

def clean(user_id):
    utils.create_user(user_id)
    path = f"data/{user_id}/shopping.json"
    with open(path, "w") as f:
        f.write("{}")
    return show_list(user_id)