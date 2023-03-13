import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Set up configuration variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Define the bot behavior
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I'm a bot!")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# Create the Updater and attach handlers
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text & ~Filters.command, echo)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

# Start the bot
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', '8443'))
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=BOT_TOKEN)
    updater.bot.setWebhook(f"https://{os.environ.get('HEROKU_APP_NAME')}.herokuapp.com/{BOT_TOKEN}")
    updater.idle()
