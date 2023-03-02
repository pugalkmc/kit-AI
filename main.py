import requests
import json
import telegram
import os
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

# ChatGPT API endpoint
CHATGPT_ENDPOINT = "https://api.openai.com/v1/engines/davinci-codex/completions"

# ChatGPT API key
CHATGPT_API_KEY = os.environ.get('VARIABLE_NAME')

# Telegram bot token
TELEGRAM_BOT_TOKEN = "5325072620:AAF3z2mQqmpyfyM9tkbNgcDn0L7-kBaEJOw"

# Create a Telegram bot instance
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)


def handle_message(update, context):
    # Get the message text
    message_text = update.message.text
    message = update.message
    chat_id = update.effective_chat.id

    # Call the ChatGPT API to generate a response
    # Call the ChatGPT API to generate a response
    # Call the ChatGPT API to generate a response
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {CHATGPT_API_KEY}"
    }
    data = {
    "prompt": f"Context: {message_text}",
    "max_tokens": 200,
    "temperature": 0.8
    }
    response = requests.post(CHATGPT_ENDPOINT, headers=headers, data=json.dumps(data))
    response_text = response.json()["choices"][0]["text"].strip()

    # Extract the code portion of the response text
    code_start = response_text.find('```')
    code_end = response_text.rfind('```')
    if code_start != -1 and code_end != -1:
        code_text = response_text[code_start+len('```'):code_end].strip()
    else:
        code_text = response_text

    # Format the code text as monospace text
        response_data = response_text.replace(code_text, f"<code>{code_text}</code>")


    # Check if the response is empty or contains an error message
    if not response_data:
        response_text = "Sorry, I couldn't generate a response for that."
    elif "model_failure" in response_data:
        response_text = "Sorry, there was an error generating the response."
    else:
        response_text = response_data

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
