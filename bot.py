from collections import defaultdict
from telegram.ext import Updater, CommandHandler
import shopping
import my_calendar
import datetime as dt
import dateutil.parser as dtparser

def start(update, context):
    name = update.message.chat.first_name
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f"Hi {name}!"
    )

def parse_add_shopping_list(args):
    if len(args) == 1:
        raise ValueError()
    items = defaultdict(int)
    forced_word = False
    prev_num = 1
    if args[-1].isdigit():
        raise ValueError()
    for word in args[1:]:
        if word.isdigit():
            if forced_word:
                raise ValueError()
            num = int(word)
            if num == 0:
                raise ValueError()
            prev_num = num
            forced_word = True
        else:
            forced_word = False
            items[word] += prev_num
            prev_num = 1
    return items

def parse_remove_shopping_list(args):
    if len(args) == 1:
        raise ValueError()
    items = set()
    for word in args[1:]:
        if word.isdigit():
            raise ValueError()
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
            to_buy = parse_add_shopping_list(args)
            message = shopping.add(user_id, to_buy)
        elif args[0] == "remove":
            to_remove = parse_remove_shopping_list(args)
            message = shopping.remove(user_id, to_remove)
        elif len(args) == 1 and args[0] == "clear":
            message = shopping.clear(user_id)
        else:
            raise ValueError()
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="I couldn't understand you :(")

# TODO: implement the calendar option
def parse_add_calendar(args):
    if len(args) <= 1:
        raise ValueError()
    today = dt.datetime.now()
    parsed_dt, (event_ret, *_) = dtparser.parse(
        timestr=" ".join(args), default=today, ignoretz=True, dayfirst=True, fuzzy_with_tokens=True
    )
    dt_ret = parsed_dt.strftime("%Y/%m/%d")
    return event_ret, dt_ret

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
            pass
        elif len(args) == 1 and args[0] == "clear":
            message = my_calendar.clear(user_id)
        else:
            raise ValueError()
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="I couldn't understand you :(")


# TODO: Edit distance for the remove/edit options 
# https://pypi.org/project/editdistance/0.3.1/

TOKEN = open('token.txt').read().strip()

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('shop', shop, pass_args=True))
dispatcher.add_handler(CommandHandler('calendar', calendar, pass_args=True))


updater.start_polling()