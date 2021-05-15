from io import BytesIO
import json
import os
import utils
import datetime as dt
import matplotlib.pyplot as plt
from itertools import groupby


def new(user_id, name):
    utils.create_user(user_id)
    path = f"data/{user_id}/workouts/{name}.json"
    if os.path.isfile(path):
        raise ValueError("Invalid command: this exercise already exists.")
    utils.create_json_dict(path)
    return f"Workout {name} created successfully!"


def remove(user_id, name):
    utils.create_user(user_id)
    path = f"data/{user_id}/workouts/{name}.json"
    if not os.path.isfile(path):
        raise ValueError("Invalid command: this exercise doesn't exist.")
    os.remove(path)
    return f"Workout {name} removed successfully!"

def clear(user_id):
    utils.create_user(user_id)
    for name in os.listdir(f"data/{user_id}/workouts/"):
        path = f"data/{user_id}/workouts/{name}"
        with open(path, "w") as f:
            f.write("{}")
    return f"All workouts cleared successfully!"

def add(user_id, to_add):
    utils.create_user(user_id)
    wrong_names = []
    for name, num in to_add.items():
        path = f"data/{user_id}/workouts/{name}.json"
        if not os.path.isfile(path):
            wrong_names.append(name)
        else:
            with open(path, "r") as f:
                data = json.load(f)
            today_str = dt.datetime.now().strftime("%Y/%m/%d")
            data[today_str] = data.get(today_str, 0) + num
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
    if len(wrong_names) == 0:
        return "Workout saved successfully!"
    elif len(wrong_names) == 1:
        return f"Exercise {wrong_names[0]} was not found."
    else:
        return f"Exercises {', '.join(wrong_names)} were not found"


def stats(user_id, name, period=90):
    utils.create_user(user_id)
    path = f"data/{user_id}/workouts/{name}.json"
    if not os.path.isfile(path):
        raise ValueError("Invalid command: this exercise doesn't exist.")
    with open(path, "r") as f:
        data = json.load(f)
    today = dt.datetime.now()
    days = []
    shown_days = []
    nums = []
    for diff in range(-period + 1, 1):
        day = today + dt.timedelta(days=diff)
        day_iso = day.strftime("%Y/%m/%d")
        days.append(day.strftime("%d/%m/%Y"))
        shown_days.append(day.strftime("%d %b") if diff % 3 == 0 else "")
        nums.append(data.get(day_iso, 0))

    binary = [1 if x != 0 else 0 for x in nums]
    streaks = [len(list(g)) for k, g in groupby(binary) if k == 1]
    max_num = max(nums)
    max_day = days[nums.index(max_num)]
    avg = sum(nums) / period
    yearly = int(avg * 365)
    workout_days = sum([x != 0 for x in nums])
    best_streak = 0 if len(streaks) == 0 else max(streaks)
    curr_streak = 0 if len(streaks) == 0 else streaks[-1]

    msg = f"""
*{name.title()} stats for the last {period} days*
\\* Maximum: {max_num} ({max_day})
\\* Daily average: {avg:.1f}
\\* Yearly projected total: {yearly}
\\* You've been active {workout_days} days
\\* Best activity streak: {best_streak}
\\* Current activity streak: {curr_streak}
    """

    figure = plt.gcf()
    figure.set_size_inches(16, 9)
    plt.xticks(rotation=45, ha="right")
    plt.bar(range(period), nums, align="center", alpha=0.8)
    plt.xticks(range(period), shown_days)
    plt.title(name.title())
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    buf.seek(0)
    plt.close()
    return buf, msg
