from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from PIL import Image, ImageGrab
import os
import logging
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# from mcf_build import MCFWindow

# app_tg_blueprint = MCFWindow()

async def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    if update.message.text == '/g':
        # screen = ImageGrab.grab()
        try:
            with open(os.path.join('images_lib', 'scorecrop.png'), 'rb') as photo_file:
                await update.message.reply_photo(photo=photo_file)
        except:
            await update.message.reply_text('Нет активной игры')
       


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()
    g_handler = CommandHandler('g', echo)
    application.add_handler(g_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# def start_polling():
main()