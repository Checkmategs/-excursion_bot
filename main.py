import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from flask import Flask, request
import threading
import os

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация Flask приложения
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    # Здесь можно добавить обработку вебхуков если потребуется
    return "OK", 200

# Данные экскурсии с обложками
TOUR_DATA = {
    # ... (остается без изменений)
}

# Текущая точка для каждого пользователя
user_states = {}

# ... (все остальные функции остаются без изменений до main())

def run_bot():
    """Запуск Telegram бота в отдельном потоке"""
    application = Application.builder().token(os.getenv("TELEGRAM_TOKEN", "7431332809:AAEKuhntXgihb_KbHdfBrR3vGAzfxOx4eeI")).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('menu', show_main_menu))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    application.run_polling()

def main():
    """Основная функция запуска"""
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Запускаем Flask сервер
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 10000)))

if __name__ == '__main__':
    main()