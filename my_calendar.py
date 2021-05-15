import json
import utils

def show_date(date):
    return date

def show_calendar(user_id):
    utils.create_user(user_id)
    path = f"data/{user_id}/calendar.json"
    with open(path, "r") as f:
        current = json.load(f)
    if len(current) == 0:
        return "Youhave no events in your calendar."
    lines = ["Future events:"] + [
        f"* {name}: {show_date(date)}"
        for name, date in current.items()
    ]
    return "\n".join(lines)

def add(user_id, event, date):
    utils.create_user(user_id)
    path = f"data/{user_id}/calendar.json"
    with open(path, "r") as f:
        current = json.load(f)
    current[event] = date
    with open(path, "w") as f:
        json.dump(current, f, indent=4)
    return show_list(user_id)