from collections import defaultdict
from telegram.ext import Updater, CommandHandler
import validators
import shopping
import my_calendar
import datetime as dt
import dateutil.parser as dtparser
import links


def start(update, context):
    name = update.message.chat.first_name
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hi {name}!")


def get_id(update, context):
    user_id = update.message.chat.id
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{user_id}")


def parse_add_shopping_list(args):
    if len(args) == 0:
        raise ValueError("Invalid command: nothing to buy.")
    items = defaultdict(int)
    forced_word = False
    prev_num = 1
    if args[-1].isdigit():
        raise ValueError("Invalid command: ends with a number.")
    for word in args:
        if word.isdigit():
            if forced_word:
                raise ValueError("Invalid command: two consecutive numbers.")
            num = int(word)
            if num == 0:
                raise ValueError("Invalid command: can't buy 0 things.")
            prev_num = num
            forced_word = True
        else:
            forced_word = False
            items[word] += prev_num
            prev_num = 1
    return items


def parse_remove_shopping_list(args):
    if len(args) == 0:
        raise ValueError("Invalid command: nothing to remove.")
    items = set()
    for word in args:
        if word.isdigit():
            raise ValueError(f"Invalid command: {word} is a number.")
        else:
            items.add(word)
    return items


def shop(update, context):
    user_id = update.message.chat.id
    args = context.args

    try:
        if len(args) == 0 or (len(args) == 1 and args[0] in ["list", "show"]):
            message = shopping.show_list(user_id)
        elif args[0] == "add":
            to_buy = parse_add_shopping_list(args[1:])
            message = shopping.add(user_id, to_buy)
        elif args[0] == "remove":
            to_remove = parse_remove_shopping_list(args[1:])
            message = shopping.remove(user_id, to_remove)
        elif len(args) == 1 and args[0] == "clear":
            message = shopping.clear(user_id)
        else:
            raise ValueError("I couldn't understand you :(")
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))


def shopgroup(update, context):
    user_id = update.message.chat.id
    args = context.args

    try:
        if len(args) == 0 or (len(args) == 1 and args[0] == "list"):
            message = shopping.show_shopgroups_list(user_id)
        elif len(args) == 1 or (len(args) == 2 and args[1] == "list"):
            message = shopping.show_list(user_id, args[0])
        elif args[0] == "create":
            if len(args) != 3:
                raise ValueError(
                    "Invalid command: try /shopgroup create <groupname> <password>"
                )
            message = shopping.create_shopgroup(user_id, args[1], args[2])
        elif args[0] == "join":
            if len(args) != 3:
                raise ValueError(
                    "Invalid command: try /shopgroup join <groupname> <password>"
                )
            message = shopping.join_shopgroup(user_id, args[1], args[2])
        elif args[0] == "leave":
            if len(args) != 2:
                raise ValueError("Invalid command: try /shopgroup leave <groupname>")
            message = shopping.leave_shopgroup(user_id, args[1])
        elif args[1] == "add":
            to_buy = parse_add_shopping_list(args[2:])
            message = shopping.add(user_id, to_buy, args[0])
        elif args[1] == "remove":
            to_remove = parse_remove_shopping_list(args[2:])
            message = shopping.remove(user_id, to_remove, args[0])
        elif args[1] == "clear":
            message = shopping.clear(user_id, args[0])
        else:
            raise ValueError("I couldn't understand you :(")
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))

# TODO: implement the calendar option
def parse_add_calendar(args):
    if len(args) <= 1:
        raise ValueError()
    today = dt.datetime.now()
    parsed_dt, (event_ret, *_) = dtparser.parse(
        timestr=" ".join(args), default=today, ignoretz=True, dayfirst=True, fuzzy_with_tokens=True
    )
    dt_ret = parsed_dt.strftime("%Y/%m/%d")
    return event_ret.strip(), dt_ret

def calendar(update, context):
    user_id = update.message.chat.id
    args = context.args

    try:
        if len(args) == 0 or (len(args) == 1 and args[0] == "show"):
            message = my_calendar.show_calendar(user_id)
        elif args[0] == "add":
            event, date = parse_add_calendar(args[1:])
            message = my_calendar.add(user_id, event, date)
        elif args[0] == "remove":
            message = my_calendar.remove(user_id, " ".join(args[1:]))
        elif len(args) == 1 and args[0] == "clear":
            message = my_calendar.clear(user_id)
        else:
            raise ValueError("Calendar error")
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))


def parse_add_link(args):
    if len(args) != 2:
        raise ValueError("Invalid command: try /link add <name> <url>")
    name, url = args
    if validators.url(name):
        raise ValueError("Invalid command: try /link add <name> <url>")
    if not validators.url(url):
        raise ValueError(f"Invalid command: {url} is not a valid url")
    return name, url


def link(update, context):
    user_id = update.message.chat.id
    args = context.args

    try:
        if len(args) == 0 or (len(args) == 1 and args[0] == "list"):
            message = links.show_list(user_id)
        elif args[0] == "add":
            name, url = parse_add_link(args[1:])
            message = links.add(user_id, name, url)
        elif len(args) == 2 and args[0] == "remove":
            message = links.remove(user_id, args[1])
        elif len(args) == 1 and args[0] == "clear":
            message = links.clear(user_id)
        elif len(args) == 1:
            message = links.get(user_id, args[0])
        else:
            raise ValueError("I couldn't understand you :(")
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))


# TODO: Edit distance for the remove/edit options
# https://pypi.org/project/editdistance/0.3.1/

TOKEN = open("token.txt").read().strip()

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

<<<<<<< HEAD
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('id', get_id))
dispatcher.add_handler(CommandHandler('shop', shop, pass_args=True))
dispatcher.add_handler(CommandHandler('calendar', calendar, pass_args=True))
dispatcher.add_handler(CommandHandler('shopgroup', shopgroup, pass_args=True))
=======
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("id", get_id))
dispatcher.add_handler(CommandHandler("shop", shop, pass_args=True))
dispatcher.add_handler(CommandHandler("shopgroup", shopgroup, pass_args=True))
dispatcher.add_handler(CommandHandler("link", link, pass_args=True))
>>>>>>> a2d415a9c1cc39f44abab205755ff29fb3f77b5b

updater.start_polling()
