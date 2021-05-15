from telegram.ext import Updater, CommandHandler

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola! Soc un bot bàsic.")

def repeat(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=" ".join(context.args))

TOKEN = open('token.txt').read().strip()

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('repeat', repeat, pass_args=True))

updater.start_polling()