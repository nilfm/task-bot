import json
import utils


def show_list(user_id):
    utils.create_user(user_id)
    path = f"data/{user_id}/links.json"
    with open(path, "r") as f:
        data = json.load(f)
    lines = ["Your links:"] + [f"\\* {name}: {url}" for name, url in data.items()]
    return "\n".join(lines)


def add(user_id, name, url):
    utils.create_user(user_id)
    path = f"data/{user_id}/links.json"
    with open(path, "r") as f:
        data = json.load(f)
    data[name] = url
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    return "Your link was added successfully!"


def remove(user_id, name):
    utils.create_user(user_id)
    path = f"data/{user_id}/links.json"
    with open(path, "r") as f:
        data = json.load(f)
    if name not in data:
        raise ValueError("Invalid command: link name not found.")
    data.pop(name, None)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    return "Your link was removed successfully!"


def get(user_id, name):
    utils.create_user(user_id)
    path = f"data/{user_id}/links.json"
    with open(path, "r") as f:
        data = json.load(f)
    if name not in data:
        raise ValueError("Invalid command: link name not found")
    return data[name]


def clear(user_id, name):
    utils.create_user(user_id)
    path = f"data/{user_id}/links.json"
    with open(path, "w") as f:
        f.write("{}")
    return f"Links cleared successfully"
