import os
import logging
import re
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Set up configuration variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

# Define the bot behavior
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I'm a bot!")

def search_youtube(query):
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={YOUTUBE_API_KEY}'
    response = requests.get(url).json()
    video_id = response['items'][0]['id']['videoId']
    return f'https://www.youtube.com/watch?v={video_id}'

def echo(update, context):
    message = update.message.text
    if re.match(r'^https?:\/\/(?:www\.)?youtube.com\/watch\?.*v=([^\s&]+)', message):
        query = message.split('v=')[1]
        context.bot.send_message(chat_id=update.effective_chat.id, text=search_youtube(query))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

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
