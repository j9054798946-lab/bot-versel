import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from flask import Flask, request
import time
import json

# --- Configuration ---
# Load environment variables. These must be set in your Vercel project settings.
TOKEN = os.environ.get('TELEGRAM_TOKEN')
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET')
PUBLIC_URL = os.environ.get('PUBLIC_URL')

# A fatal error will occur on Vercel if these are not set.
if not TOKEN or not WEBHOOK_SECRET or not PUBLIC_URL:
    raise ValueError("FATAL ERROR: TELEGRAM_TOKEN, WEBHOOK_SECRET, and PUBLIC_URL environment variables must be set.")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


# --- Bot Logic (Menus and Handlers from your original file) ---

# Главное меню
def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    video_button = InlineKeyboardButton("📹 Видеоматериалы", callback_data='video_menu')
    contacts_button = InlineKeyboardButton("📞 Контакты", callback_data='contacts_menu')
    request_button = InlineKeyboardButton("✍️ Оставить заявку", callback_data='make_request')
    reviews_button = InlineKeyboardButton("💬 Отзывы", callback_data='reviews_menu')
    faq_button = InlineKeyboardButton("❓ Частые вопросы", callback_data='faq_menu')
    price_button = InlineKeyboardButton("💰 Прайс", callback_data='show_price')
    reserve_button = InlineKeyboardButton("🔒 Резерв", callback_data='reserve')
    markup.add(video_button)
    markup.add(contacts_button, request_button)
    markup.add(reviews_button, faq_button)
    markup.add(price_button, reserve_button)
    return markup

# Меню видеоматериалов
def video_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    for i in range(1, 6):
        markup.add(InlineKeyboardButton(f"Ссылка {i}", callback_data=f'video_link_{i}'))
    markup.add(InlineKeyboardButton("⬅️ Назад", callback_data='back_to_main'))
    return markup

# Меню контактов
def contacts_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("📍 Наш адрес", callback_data='contact_address'))
    markup.add(InlineKeyboardButton("📧 Email", callback_data='contact_email'))
    markup.add(InlineKeyboardButton("📱 Телефон", callback_data='contact_phone'))
    markup.add(InlineKeyboardButton("💬 Telegram", callback_data='contact_telegram'))
    markup.add(InlineKeyboardButton("🌐 Сайт", callback_data='contact_website'))
    markup.add(InlineKeyboardButton("⬅️ Назад", callback_data='back_to_main'))
    return markup

# Меню отзывов
def reviews_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    for i in range(1, 6):
        markup.add(InlineKeyboardButton(f"Отзыв {i}", callback_data=f'review_link_{i}'))
    markup.add(InlineKeyboardButton("⬅️ Назад", callback_data='back_to_main'))
    return markup

# Меню частых вопросов
def faq_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    questions = ["Как сделать заказ?", "Какие способы оплаты?", "Сколько идет доставка?", "Как вернуть товар?", "Есть ли скидки?"]
    for i, question in enumerate(questions, 1):
        markup.add(InlineKeyboardButton(f"Вопрос {i}: {question}", callback_data=f'faq_question_{i}'))
    markup.add(InlineKeyboardButton("⬅️ Назад", callback_data='back_to_main'))
    return markup

# Меню оплаты
def payment_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("💳 СБП (по номеру)", callback_data='payment_sbp'), InlineKeyboardButton("💳 Банковская карта", callback_data='payment_card'))
    markup.add(InlineKeyboardButton("⬅️ Назад", callback_data='back_to_main'))
    return markup

# Меню прайс-листа с кнопкой "назад"
def price_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("⬅️ Назад", callback_data='back_to_main_from_price'))
    return markup

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "👋 Добро пожаловать! Выберите интересующий раздел:", reply_markup=main_menu())

# Обработчик callback-кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        if call.data == 'video_menu':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="📹 Видеоматериалы:", reply_markup=video_menu())
        elif call.data == 'contacts_menu':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="📞 Наши контакты:", reply_markup=contacts_menu())
        elif call.data == 'make_request':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="✍️ Для оформления заявки на консультацию, пожалуйста, выберите способ оплаты:", reply_markup=payment_menu())
        elif call.data == 'reviews_menu':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="💬 Отзывы наших клиентов:", reply_markup=reviews_menu())
        elif call.data == 'faq_menu':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="❓ Частые вопросы:", reply_markup=faq_menu())
        elif call.data == 'show_price':
            bot.answer_callback_query(call.id)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            # NOTE: File sending from a serverless function can be tricky.
            # The file 'price.xlsx' must be in the same directory as this index.py file.
            file_path = os.path.join(os.path.dirname(__file__), 'price.xlsx')
            if os.path.exists(file_path):
                with open(file_path, 'rb') as price_file:
                    bot.send_document(call.message.chat.id, price_file, caption="💰 Актуальный прайс-лист на консультации", reply_markup=price_menu())
            else:
                bot.send_message(call.message.chat.id, "❌ Файл прайс-листа не найден. Пожалуйста, ��ообщите администратору.", reply_markup=main_menu())
        elif call.data == 'reserve':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🔒 Функция резервирования временно недоступна. Мы работаем над её внедрением!", reply_markup=main_menu())
        elif call.data == 'back_to_main':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "👋 Главное меню:", reply_markup=main_menu())
        elif call.data == 'back_to_main_from_price':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "👋 Главное меню:", reply_markup=main_menu())
        elif call.data.startswith('video_link_'):
            link_num = call.data.split('_')[-1]
            bot.answer_callback_query(call.id, f"Видео {link_num}")
        elif call.data.startswith('review_link_'):
            link_num = call.data.split('_')[-1]
            bot.answer_callback_query(call.id, f"Отзыв {link_num}")
        elif call.data.startswith('faq_question_'):
            q_num = call.data.split('_')[-1]
            bot.answer_callback_query(call.id, f"Ответ на вопрос {q_num}")
        elif call.data.startswith('contact_'):
            contact_type = call.data.split('_')[-1]
            contact_info = {'address': '📍 Наш адрес: ...', 'email': '📧 Email: ...', 'phone': '📱 Телефон: ...', 'telegram': '💬 Telegram: ...', 'website': '🌐 Сайт: ...'}
            bot.answer_callback_query(call.id, contact_info.get(contact_type, "Информация недоступна"))
        elif call.data == 'payment_sbp':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="💳 *Оплата через СБП* ...", parse_mode='Markdown', reply_markup=main_menu())
        elif call.data == 'payment_card':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="💳 *Оплата банковской картой* ...", parse_mode='Markdown', reply_markup=main_menu())
    except Exception as e:
        print(f"Error in callback handler: {e}")


# --- Main Webhook Handler (from Template) ---
@app.route('/', methods=['GET', 'POST'])
def webhook_and_index():
    if request.method == 'GET':
        return "Bot is running!", 200
    if request.method == 'POST':
        secret_header = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
        if secret_header != WEBHOOK_SECRET:
            return "Unauthorized", 401
        try:
            raw_data = request.stream.read().decode('utf-8')
            update = telebot.types.Update.de_json(raw_data)
            print("Update received, passing to bot processor.")
            # Let the bot's internal router handle all update types
            bot.process_new_updates([update])
        except Exception as e:
            print(f"An error occurred in webhook handler: {e}")
        return 'OK', 200

# --- Setup Endpoint (from Template) ---
@app.route('/set_webhook')
def set_webhook():
    url = f"https://{PUBLIC_URL}/"
    bot.remove_webhook()
    bot.set_webhook(url=url, secret_token=WEBHOOK_SECRET)
    return f"Webhook successfully set to {url}"