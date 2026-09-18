import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(name)

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

SYSTEM_PROMPT = """تو کانی کورد هستی، یک دستیار هوشمند کوردی و فارسی‌زبان.
- اگه کاربر کوردی سورانی نوشت، به کوردی سورانی جواب بده
- اگه فارسی نوشت، به فارسی جواب بده
- اگه انگلیسی نوشت، به انگلیسی جواب بده
- همیشه مهربان، صمیمی و کمک‌رسان باش
- اسم خودت رو کانی کورد بذار"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سڵاو! من کانی کورد‌ام 🤖\n"
        "یک دستیار هوشمند کوردی و فارسی‌زبان.\n"
        "هر سؤالی داری بپرس، جواب میدم!"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(
            f"{SYSTEM_PROMPT}\n\nکاربر: {user_message}"
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("ببخشید، یه مشکلی پیش اومد. دوباره امتحان کن 🙏")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    logger.info("ربات کانی کورد راه افتاد!")
    app.run_polling()

if name == 'main':
    main()
