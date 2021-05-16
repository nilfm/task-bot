from collections import defaultdict
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import validators
import shopping
import my_calendar
import datetime as dt
import dateutil.parser as dtparser
import links
import workouts
import enhance
import PIL.Image as Image
import io


def start(update, context):
    name = update.message.chat.first_name
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hi {name}! Try /help for an explanation of all my commands.")


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
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))


def shopgroup(update, context):
    user_id = update.message.chat.id
    args = context.args

    try:
        if len(args) == 0 or (len(args) == 1 and args[0] in ["list", "show"]):
            message = shopping.show_shopgroups_list(user_id)
        elif len(args) == 1 or (len(args) == 2 and args[1] in ["list", "show"]):
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
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))


def parse_add_calendar(args):
    if len(args) <= 1:
        raise ValueError()
    today = dt.datetime.now()
    parsed_dt, (event_ret, *_) = dtparser.parse(
        timestr=" ".join(args),
        default=today,
        ignoretz=True,
        dayfirst=True,
        fuzzy_with_tokens=True,
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
            raise ValueError("I couldn't understand you :(")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
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
        if len(args) == 0 or (len(args) == 1 and args[0] in ["list", "show"]):
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
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))


def parse_add_workout(args):
    if len(args) == 0:
        raise ValueError("Invalid command: nothing to add.")
    if len(args) % 2 != 0:
        raise ValueError("Invalid command: odd length of argument list.")
    items = defaultdict(int)

    for num, name in zip(args[::2], args[1::2]):
        if not num.isdigit():
            raise ValueError(f"Invalid command: {num} is not a number")
        num = int(num)
        if num == 0:
            raise ValueError(f"Invalid command: can't buy 0 {name}")
        items[name] += num

    return items


def workout(update, context):
    user_id = update.message.chat.id
    args = context.args

    try:
        if len(args) == 0:
            raise ValueError("Invalid command: try /help")
        elif len(args) == 2 and args[0] == "new":
            message = workouts.new(user_id, args[1])
        elif len(args) == 2 and args[0] == "remove":
            message = workouts.remove(user_id, args[1])
        elif args[0] == "add":
            to_add = parse_add_workout(args[1:])
            message = workouts.add(user_id, to_add)
        elif len(args) == 2 and args[0] == "show":
            plot, message = workouts.stats(user_id, args[1])
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=plot)
        elif len(args) == 1 and args[0] == "clear":
            message = workouts.clear(user_id)
        else:
            raise ValueError("I couldn't understand you :(")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))


def my_help(update, context):
    user_id = update.message.chat.first_name
    with open("help.md", "r") as f:
        txt = f.read()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=txt,
        parse_mode=telegram.ParseMode.MARKDOWN,
    )


def handle_photo(update, context):
    file = update.message.photo[-1].get_file()
    bytearray = file.download_as_bytearray()
    image_stream = io.BytesIO(bytearray)
    image_stream.seek(0)
    context.bot.send_photo(
        chat_id=update.effective_chat.id, photo=enhance.process(image_stream)
    )


TOKEN = open("token.txt").read().strip()

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("id", get_id))
dispatcher.add_handler(CommandHandler("shop", shop, pass_args=True))
dispatcher.add_handler(CommandHandler("shopgroup", shopgroup, pass_args=True))
dispatcher.add_handler(CommandHandler("calendar", calendar, pass_args=True))
dispatcher.add_handler(CommandHandler("link", link, pass_args=True))
dispatcher.add_handler(CommandHandler("workout", workout, pass_args=True))
dispatcher.add_handler(CommandHandler("help", my_help))
dispatcher.add_handler(MessageHandler(filters=Filters.photo, callback=handle_photo))

updater.start_polling()
