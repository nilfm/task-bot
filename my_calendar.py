import json
import utils
import datetime as dt


def show_date(date):
    ret = dt.datetime.strptime(date, "%Y/%m/%d")
    return ret.strftime("%A, %d %B %Y")

def show_calendar(user_id):
    utils.create_user(user_id)
    path = f"data/{user_id}/calendar.json"
    with open(path, "r") as f:
        current = json.load(f)
    today = dt.datetime.now()
    today_str = today.strftime("%Y/%m/%d")
    filtered = {
        name: date
        for name, date in current.items()
        if date >= today_str
    }
    if len(filtered) == 0:
        return "You have no events in your calendar."
    max_len = max([len(name) for name in filtered])
    lines = ["Future events:"] + [
        f"* {name.ljust(max_len)}  -  {show_date(date)}"
        for name, date in sorted(filtered.items(), key=lambda x: x[1])
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
    return show_calendar(user_id)

def remove(user_id, event):
    utils.create_user(user_id)
    path = f"data/{user_id}/calendar.json"
    with open(path, "r") as f:
        current = json.load(f)
    current.pop(event, None)
    with open(path, "w") as f:
        json.dump(current, f, indent=4)
    return show_calendar(user_id)

def clear(user_id):
    utils.create_user(user_id)
    path = f"data/{user_id}/calendar.json"
    with open(path, "w") as f:
        f.write("{}")
    return show_calendar(user_id)
