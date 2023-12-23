from telegram import Update
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackContext
import os
import logging
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext):
    keyboard = [ [KeyboardButton('/game'), KeyboardButton('/build')] ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text('Выберите вариант:', reply_markup=reply_markup)


async def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    if update.message.text == '/game':
        sendable_file = 'scorecrop.png'
    elif update.message.text == '/build':
        sendable_file = 'buildcrop.png'
   
    try:
        with open(os.path.join('images_lib', sendable_file), 'rb') as photo_file:
            await update.message.reply_photo(photo=photo_file)
    except:
        await update.message.reply_text('Нет активной игры')
       
def main() -> None:
    """Start the bot."""
    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()
    g_handler = CommandHandler('game', echo)
    b_handler = CommandHandler('build', echo)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(g_handler)
    application.add_handler(b_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()