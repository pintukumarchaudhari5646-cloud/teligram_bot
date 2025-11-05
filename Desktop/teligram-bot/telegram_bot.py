from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import os

# Environment variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 नमस्ते! मैं आपका सहायक 🤖 हूँ।\nआप मुझसे कोई भी सवाल ❓ पूछ सकते हैं।"
    )

# User messages
def handle_message(update: Update, context: CallbackContext):
    # Step 1: please wait message
    update.message.reply_text("⏳ कृपया प्रतीक्षा करें...")

    user_text = update.message.text

    # Step 2: Gemini API call
    try:
        response = requests.post(
            "https://api.gemini.com/v1/ask",  # Replace with actual Gemini endpoint
            headers={"Authorization": f"Bearer {GEMINI_API_KEY}"},
            json={"prompt": user_text}
        )
        answer = response.json().get("answer", "माफ़ करें, उत्तर नहीं मिल सका।")
    except Exception as e:
        answer = "⚠️ कोई त्रुटि हुई, कृपया बाद में प्रयास करें।"

    # Step 3: Send answer to user
    update.message.reply_text(answer)

def main():
    updater = Updater(TELEGRAM_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
