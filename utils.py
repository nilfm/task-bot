import os

def create_json_dict(path):
    if not os.path.isfile(path):
        with open(path, "w") as f:
            f.write("{}")

def create_user(user_id):
    path = f"data/{user_id}"
    os.makedirs(path, exist_ok=True)
    shopping_path = f"{path}/shopping.json"
    create_json_dict(shopping_path)
    calendar_path = f"{path}/calendar.json"
    create_json_dict(calendar_path)