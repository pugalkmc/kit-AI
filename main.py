import requests
import json
import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

# ChatGPT API endpoint
CHATGPT_ENDPOINT = "https://api.openai.com/v1/engines/davinci-codex/completions"

# ChatGPT API key
CHATGPT_API_KEY = "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"

# Telegram bot token
TELEGRAM_BOT_TOKEN = "5325072620:AAF3z2mQqmpyfyM9tkbNgcDn0L7-kBaEJOw"

# Create a Telegram bot instance
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)


# Define a function to handle user messages
def handle_message(update, context):
    # Get the message text
    message_text = update.message.text

    # Call the ChatGPT API to generate a response
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHATGPT_API_KEY}"
    }
    data = {
        "prompt": message_text,
        "max_tokens": 50,
        "temperature": 0.5
    }
    response = requests.post(CHATGPT_ENDPOINT, headers=headers, data=json.dumps(data))
    response_text = response.json()["choices"][0]["text"].strip()

    # Send the response back to the user
    chat_id = update.effective_chat.id
    bot.send_message(chat_id=chat_id, text=response_text)


# Define a function to handle the /start command
def handle_start(update, context):
    chat_id = update.effective_chat.id
    bot.send_message(chat_id=chat_id,
                     text="Hello! I'm a ChatGPT bot. Send me a message and I'll generate a response for you.")


# Create a Telegram updater instance and attach the handlers
updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", handle_start))
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

# Start the bot
updater.start_polling()
updater.idle()
