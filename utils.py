import os
import json
import hashlib
from sys import path_hooks, path_importer_cache

def create_json_dict(path):
    if not os.path.isfile(path):
        with open(path, "w") as f:
            f.write("{}")

def create_json_list(path):
    if not os.path.isfile(path):
        with open(path, "w") as f:
            f.write("[]")

def hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def create_user(user_id):
    path = f"data/{user_id}"
    os.makedirs(path, exist_ok=True)
    shopping_path = f"{path}/shopping.json"
    create_json_dict(shopping_path)
    calendar_path = f"{path}/calendar.json"
    create_json_dict(calendar_path)
    shopgroups_path = f"{path}/shopgroups.json"
    create_json_list(shopgroups_path)

def update_shopgroup_list(group_id, password):
    path_dir = "data"
    path = f"{path_dir}/shopgroup_credentials.json"
    os.makedirs(path_dir, exist_ok=True)
    create_json_dict(path)
    with open(path, "r") as f:
        credentials = json.load(f)
    credentials[group_id] = hash(password)
    with open(path, "w") as f:
        json.dump(credentials, f, indent=4)

# Raises exception if group doesn't exist or if password is incorrect
def authenticate_shopgroup(group_id, password):
    path_dir = "data"
    path = f"{path_dir}/shopgroup_credentials.json"
    os.makedirs(path_dir, exist_ok=True)
    create_json_dict(path)
    with open(path, "r") as f:
        credentials = json.load(f)
    if group_id not in credentials:
        raise ValueError("Invalid command: this group does not exist.")
    if credentials[group_id] != hash(password):
        raise ValueError("Invalid credentials: wrong shopgroup name or password.")

# Raises exception if user doesn't belong to group
def verify_shopgroup(user_id, group_id):
    path = f"data/{user_id}/shopgroups.json"
    with open(path, "r") as f:
        current = json.load(f)
    if group_id not in current:
        raise ValueError("Invalid command: you are not part of this shopgroup.")

def add_user_to_shopgroup(user_id, group_id):
    path = f"data/{user_id}/shopgroups.json"
    path_info = f"data/shopgroup_info/{group_id}.json"
    with open(path, "r") as f:
        current = json.load(f)
    if group_id in current:
        raise ValueError("Invalid command: you were already in this shopgroup.")
    current.append(group_id)
    with open(path, "w") as f:
        json.dump(current, f, indent=4)

    with open(path_info, "r") as f:
        info = json.load(f)
    info.append(user_id)

    with open(path_info, "w") as f:
        json.dump(info, f, indent=4)

def remove_user_from_shopgroup(user_id, group_id):
    path = f"data/{user_id}/shopgroups.json"
    path_info = f"data/shopgroup_info/{group_id}.json"

    with open(path, "r") as f:
        current = json.load(f)
    if group_id not in current:
        raise ValueError("Invalid command: you were not in this shopgroup.")
    current.remove(group_id)
    with open(path, "w") as f:
        json.dump(current, f, indent=4)

    with open(path_info, "r") as f:
        info = json.load(f)
    info.remove(user_id)

    with open(path_info, "w") as f:
        json.dump(info, f, indent=4)

    if len(info) == 0:
        delete_shopgroup(group_id)

def delete_shopgroup(group_id):
    path_shopgroup = f"data/shopgroups/{group_id}.json"
    path_info = f"data/shopgroup_info/{group_id}.json"
    path_credentials = f"data/shopgroup_credentials.json"
    os.remove(path_info)
    os.remove(path_shopgroup)
    with open(path_credentials, "r") as f:
        data = json.load(f)
    data.pop(group_id, None)
    with open(path_credentials, "w") as f:
        json.dump(data, f, indent=4)