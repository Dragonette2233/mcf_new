from telegram import Update
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler
import json
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
    keyboard = [ [KeyboardButton('/game'), KeyboardButton('/build')], [KeyboardButton('/stats_check')] ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text('Здарова, тварына', reply_markup=reply_markup)

async def echo_score(update: Update, context: CallbackContext) -> None:
    
    with open(os.path.join('.', 'arambot_lib', 'activegame_score.json'), 'r') as file:
        score_data = json.load(file)

    if score_data['is_active']:
        with open(os.path.join('.', 'arambot_lib', 'score_answer_sample.txt'), 'r', encoding='utf-8') as sample:
            message_sample = sample.read()

        # 🐳 Киллы: {blue_kills} | Башни: {blue_towers}
        # 🐙 Киллы: {red_kills} | Башни: {red_towers}
        timestamp = divmod(score_data['time'], 60)
        minutes = timestamp[0] if timestamp[0] > 9 else f"0{timestamp[0]}"
        seconds = timestamp[1] if timestamp[1] > 9 else f"0{timestamp[1]}"
        message_for_reply = message_sample.format(
            blue_kills = score_data['blue_kills'],
            blue_towers = score_data['blue_towers'],
            red_kills = score_data['red_kills'],
            red_towers = score_data['red_towers'],
            time = ':'.join([str(minutes), str(seconds)]),
        )
        await update.message.reply_text(message_for_reply)
    else:
        await update.message.reply_text('Нет активной игры')

async def echo_build(update: Update, context: CallbackContext) -> None:
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

async def stats_check(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    with open(os.path.join('.', 'arambot_lib', 'debug_stats.json'), 'r', encoding='utf-8') as js_stats:
        stats_register = json.load(js_stats)
        message = f"Результат по стате | + ({stats_register['PLUS']}) - ({stats_register['minus']})"
        await update.message.reply_text(message)
       
def main() -> None:
    """Start the bot."""
    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()
    # stats_handler = MessageHandler('s_check', stats_check)
    # g_handler = CommandHandler('game', echo)
    # b_handler = CommandHandler('build', echo)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler('game', echo_score))
    application.add_handler(CommandHandler('build', echo_build))
    application.add_handler(CommandHandler('stats_check', stats_check))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()