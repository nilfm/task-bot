import json
import utils
import os

def show_list(user_id, group_id=None):
    utils.create_user(user_id)
    path = f"data/{user_id}/shopping.json"

    if group_id is not None:
        utils.verify_shopgroup(user_id, group_id)
        path = f"data/shopgroups/{group_id}.json"

    with open(path, "r") as f:
        current = json.load(f)
    if len(current) == 0:
        return "Your shopping list is empty."
    lines = ["Your shopping list:"] + [
        f"* {name}: {amt}"
        for name, amt in current.items()
    ]
    return "\n".join(lines)

def add(user_id, to_buy, group_id=None):
    utils.create_user(user_id)
    path = f"data/{user_id}/shopping.json"

    if group_id is not None:
        utils.verify_shopgroup(user_id, group_id)
        path = f"data/shopgroups/{group_id}.json"

    with open(path, "r") as f:
        current = json.load(f)
    for name, amt in to_buy.items():
        current[name] = current.get(name, 0) + amt
    with open(path, "w") as f:
        json.dump(current, f, indent=4)
    return show_list(user_id, group_id)

def remove(user_id, to_remove, group_id=None):
    utils.create_user(user_id)
    path = f"data/{user_id}/shopping.json"

    if group_id is not None:
        utils.verify_shopgroup(user_id, group_id)
        path = f"data/shopgroups/{group_id}.json"

    with open(path, "r") as f:
        current = json.load(f)
    for name in to_remove:
        current.pop(name, None)
    with open(path, "w") as f:
        json.dump(current, f, indent=4)
    return show_list(user_id, group_id) 

def clear(user_id, group_id=None):
    utils.create_user(user_id)
    path = f"data/{user_id}/shopping.json"

    if group_id is not None:
        utils.verify_shopgroup(user_id, group_id)
        path = f"data/shopgroups/{group_id}.json"

    with open(path, "w") as f:
        f.write("{}")
    return show_list(user_id, group_id)

def create_shopgroup(user_id, group_id, password):
    utils.create_user(user_id)
    path_dir = "data/shopgroups"
    path = f"{path_dir}/{group_id}.json"
    if os.path.isfile(path):
        raise ValueError("Invalid command: a shopgroup with this name already exists.")
    os.makedirs(path_dir, exist_ok=True)
    utils.create_json_dict(path)
    utils.update_shopgroup_list(group_id, password)
    utils.add_user_to_shopgroup(user_id, group_id)
    return f"Shopgroup {group_id} was successfully created!"

def join_shopgroup(user_id, group_id, password):
    utils.create_user(user_id)
    utils.authenticate_shopgroup(group_id, password)
    utils.add_user_to_shopgroup(user_id, group_id)
    return f"Joined shopgroup {group_id} successfully!"

def leave_shopgroup(user_id, group_id):
    utils.remove_user_from_shopgroup(user_id, group_id)
    return f"Left shopgroup {group_id} successfully!"