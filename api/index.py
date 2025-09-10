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

# Временный общий обработчик для отладки
@bot.message_handler(func=lambda message: True)
def debug_all_messages(message):
    print(f"[DEBUG] Received message: Chat ID={message.chat.id}, Type={message.content_type}, Text={message.text}")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(f"[Handler] Received /start command from chat ID: {message.chat.id}")
    try:
        bot.send_message(message.chat.id, "👋 Добро пожаловать! Выберите интересующий раздел:", reply_markup=main_menu())
        print(f"[Handler] Sent welcome message to chat ID: {message.chat.id}")
    except Exception as e:
        print(f"[Handler] Error sending welcome message to chat ID {message.chat.id}: {e}")

# Обработчик callback-кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        # Главное меню
        if call.data == 'video_menu':
            bot.answer_callback_query(call.id)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                print(f"Ошибка удаления сообщения: {e}")
            
            time.sleep(0.1)
            
            bot.send_message(
                call.message.chat.id,
                "📹 Видеоматериалы:",
                reply_markup=video_menu()
            )
        
        # Контакты
        elif call.data == 'contacts_menu':
            bot.answer_callback_query(call.id)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                print(f"Ошибка удаления сообщения: {e}")
            
            time.sleep(0.1)
            
            bot.send_message(
                call.message.chat.id,
                "📞 Наши контакты:",
                reply_markup=contacts_menu()
            )
        
        # Оставить заявку
        elif call.data == 'make_request':
            bot.answer_callback_query(call.id)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                print(f"Ошибка удаления сообщения: {e}")
            
            time.sleep(0.1)
            
            bot.send_message(
                call.message.chat.id,
                "✍️ Для оформления заявки на консультацию, пожалуйста, выберите способ оплаты:",
                reply_markup=payment_menu()
            )
        
        # Отзывы
        elif call.data == 'reviews_menu':
            bot.answer_callback_query(call.id)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                print(f"Ошибка удаления сообщения: {e}")
            
            time.sleep(0.1)
            
            bot.send_message(
                call.message.chat.id,
                "💬 Отзывы наших клиентов:",
                reply_markup=reviews_menu()
            )
        
        # Частые вопросы
        elif call.data == 'faq_menu':
            bot.answer_callback_query(call.id)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                print(f"Ошибка удаления сообщения: {e}")
            
            time.sleep(0.1)
            
            bot.send_message(
                call.message.chat.id,
                "❓ Частые вопросы:",
                reply_markup=faq_menu()
            )
        
        # Прайс
        elif call.data == 'show_price':
            bot.answer_callback_query(call.id)
            print("Попытка отправить прайс-лист...")

            # Удаляем текущее сообщение с меню
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
                print("Сообщение с меню удалено")
            except Exception as e:
                print(f"Ошибка удаления сообщения: {e}")

            # Небольшая задержка для надежности
            time.sleep(0.2)

            # Проверяем существование файла
            file_path = os.path.join(os.path.dirname(__file__), 'price.xlsx')
            if os.path.exists(file_path):
                print("Файл price.xlsx найден")
                try:
                    with open(file_path, 'rb') as price_file:
                        bot.send_document(
                            call.message.chat.id,
                            price_file,
                            caption="💰 Актуальный прайс-лист на консультации",
                            reply_markup=price_menu()  # Добавляем кнопку "назад"
                        )
                    print("Прайс-лист успешно отправлен")
                except Exception as e:
                    print(f"Ошибка при отправке файла: {e}")
                    bot.send_message(
                        call.message.chat.id,
                        "❌ Произошла ошибка при отправке прайс-листа. Пожалуйста, попробуйте позже.",
                        reply_markup=main_menu()
                    )
            else:
                print("Файл price.xlsx НЕ найден!")
                bot.send_message(
                    call.message.chat.id,
                    "❌ Файл прайс-листа не найден. Пожалуйста, сообщите администратору.",
                    reply_markup=main_menu()
                )
        
        # Резерв
        elif call.data == 'reserve':
            bot.answer_callback_query(call.id)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                print(f"Ошибка удаления сообщения: {e}")
            
            time.sleep(0.1)
            
            bot.send_message(
                call.message.chat.id,
                "🔒 Функция резервирования временно недоступна. Мы работаем над её внедрением!",
                reply_markup=main_menu()
            )
        
        # Возврат в главное меню
        elif call.data == 'back_to_main':
            bot.answer_callback_query(call.id)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                print(f"Ошибка удаления сообщения: {e}")
            
            time.sleep(0.1)
            
            bot.send_message(
                call.message.chat.id,
                "👋 Главное меню:",
                reply_markup=main_menu()
            )
        
        # Возврат из прайс-листа
        elif call.data == 'back_to_main_from_price':
            bot.answer_callback_query(call.id)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
                print("Сообщение с прайсом удалено")
            except Exception as e:
                print(f"Ошибка удаления сообщения с прайсом: {e}")
                bot.send_message(
                    call.message.chat.id,
                    "⚠️ Не удалось удалить предыдущее сообщение",
                    reply_markup=main_menu()
                )
                return
            
            time.sleep(0.1)
            
            bot.send_message(
                call.message.chat.id,
                "👋 Главное меню:",
                reply_markup=main_menu()
            )
        
        # Ссылки на видео
        elif call.data.startswith('video_link_'):
            link_num = call.data.split('_')[-1]
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, f"📹 Вот ссылка {link_num}: [Перейти](https://example.com/video{link_num})", parse_mode='Markdown')
        
        # Ссылки на отзывы
        elif call.data.startswith('review_link_'):
            link_num = call.data.split('_')[-1]
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, f"💬 Вот отзыв {link_num}: [Читать](https://example.com/review{link_num})", parse_mode='Markdown')
        
        # Вопросы FAQ
        elif call.data.startswith('faq_question_'):
            q_num = call.data.split('_')[-1]
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, f"❓ Ответ на вопрос {q_num}: Ответ")
        
        # Контакты
        elif call.data.startswith('contact_'):
            contact_type = call.data.split('_')[-1]
            contact_info = {
                'address': '📍 Наш адрес: г. Москва, ул. Примерная, д. 1, офис 123',
                'email': '📧 Email: info@yourcompany.com',
                'phone': '📱 Телефон: +7 905 479-89-46',
                'telegram': '💬 Telegram: @yourcompany',
                'website': '🌐 Сайт: https://yourcompany.com'
            }
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, contact_info.get(contact_type, "Информация недоступна"))
        
        # Оплата СБП
        elif call.data == 'payment_sbp':
            bot.answer_callback_query(call.id)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                print(f"Ошибка удаления сообщения: {e}")
            
            time.sleep(0.1)
            
            bot.send_message(
                call.message.chat.id,
                "💳 *Оплата через Систему Быстрых Платежей (СБП)*\n\n"
                "Для оплаты консультации:\n"
                "1. Откройте приложение вашего банка\n"
                "2. Перейдите в раздел «Платежи» → «СБП»\n"
                "3. Введите номер телефона: `+7 905 479-89-46`\n"
                "4. Укажите сумму согласно прайсу\n"
                "5. В комментарии укажите: `Консультация Telegram`\n\n"
                "После оплаты отправьте нам скриншот чека для подтверждения.",
                parse_mode='Markdown',
                reply_markup=main_menu()
            )
        
        # Оплата картой
        elif call.data == 'payment_card':
            bot.answer_callback_query(call.id)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                print(f"Ошибка удаления сообщения: {e}")
            
            time.sleep(0.1)
            
            bot.send_message(
                call.message.chat.id,
                "💳 *Оплата банковской картой*\n\n"
                "Для оплаты консультации:\n"
                "1. Перейдите по ссылке для оплаты: [Оплатить картой](https://example.com/payment)\n"
                "2. Укажите сумму согласно прайсу\n"
                "3. В комментарии укажите: `Консультация Telegram`\n\n"
                "После оплаты отправьте нам скриншот чека для подтверждения.",
                parse_mode='Markdown',
                reply_markup=main_menu()
            )
    
    except Exception as e:
        print(f"Ошибка в обработчике callback: {e}")
        bot.answer_callback_query(call.id, text="Произошла ошибка. Пожалуйста, попробуйте позже.", show_alert=True)


# --- Main Webhook Handler (from Template) ---
@app.route('/', methods=['GET', 'POST'])
def webhook_and_index():
    print("--- Request received by webhook_and_index ---")
    # --- Automatic Webhook Setup on Request (Attempt 4) ---
    # This ensures the webhook is always set to the correct URL, even after cold starts.
    try:
        target_url = f"https://{PUBLIC_URL}/"
        print(f"[Webhook Setup in Handler] Checking webhook status for: {target_url}")
        current_webhook_info = bot.get_webhook_info()

        if not current_webhook_info or current_webhook_info.url != target_url:
            print("[Webhook Setup in Handler] Webhook not set or incorrect. Attempting to set...")
            print("[Webhook Setup in Handler] Removing any existing webhook...")
            bot.remove_webhook()
            time.sleep(0.5) # Give Telegram a moment to process

            print(f"[Webhook Setup in Handler] Setting new webhook to {target_url} with secret token...")
            bot.set_webhook(url=target_url, secret_token=WEBHOOK_SECRET)
            print("[Webhook Setup in Handler] Webhook set command sent to Telegram.")

            # Verify if the webhook was set correctly (optional, but good for debugging)
            current_webhook_info_after_set = bot.get_webhook_info()
            if current_webhook_info_after_set and current_webhook_info_after_set.url == target_url:
                print(f"[Webhook Setup in Handler] Webhook successfully verified to be set to {target_url}")
            else:
                print(f"[Webhook Setup in Handler] Webhook verification failed. Current URL: {current_webhook_info_after_set.url if current_webhook_info_after_set else 'None'}")
        else:
            print(f"[Webhook Setup in Handler] Webhook already correctly set to: {current_webhook_info.url}")
    except Exception as e:
        print(f"[Webhook Setup in Handler] Error during automatic webhook setup: {e}")

    if request.method == 'GET':
        return "Bot is running!", 200
    if request.method == 'POST':
        secret_header = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
        if secret_header != WEBHOOK_SECRET:
            return "Unauthorized", 401
        try:
            raw_data = request.stream.read().decode('utf-8')
            update = telebot.types.Update.de_json(raw_data)
            print(f"[Webhook Handler] Registered message handlers: {len(bot.message_handlers)}")
            print("Update received, passing to bot processor.")
            # Let the bot's internal router handle all update types
            start_time = time.time()
            bot.process_new_updates([update])
            end_time = time.time()
            print(f"Bot processed update in {end_time - start_time:.4f} seconds.")
        except Exception as e:
            print(f"An error occurred in webhook handler: {e}")
        return 'OK', 200

# --- Setup Endpoint (Safe Version) ---
@app.route('/set_webhook')
def set_webhook_manual():
    try:
        target_url = f"https://{PUBLIC_URL}/"
        print(f"Attempting to set webhook to: {target_url}")

        # Always remove the webhook first to ensure a clean slate
        print("Removing any existing webhook...")
        bot.remove_webhook()
        time.sleep(0.5) # Give Telegram a moment to process

        print(f"Setting new webhook to {target_url} with secret token...")
        bot.set_webhook(url=target_url, secret_token=WEBHOOK_SECRET)
        print("Webhook set command sent to Telegram.")

        # Verify if the webhook was set correctly (optional, but good for debugging)
        current_webhook_info = bot.get_webhook_info()
        if current_webhook_info and current_webhook_info.url == target_url:
            print(f"Webhook successfully verified to be set to {target_url}")
            return f"Webhook successfully set and verified to {target_url}", 200
        else:
            print(f"Webhook verification failed. Current URL: {current_webhook_info.url if current_webhook_info else 'None'}")
            return f"Webhook set, but verification failed. Current URL: {current_webhook_info.url if current_webhook_info else 'None'}", 500

    except Exception as e:
        print(f"Error in set_webhook: {e}")
        return f"An error occurred: {e}", 500


