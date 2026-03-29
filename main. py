import telebot
from telebot import types

# التوكن الخاص بك (تم التحقق منه)
API_TOKEN = '8697358875:AAGaLUUDMR85ocFnM45yOUv-1iA6MXjcKyE'
bot = telebot.TeleBot(API_TOKEN)

# قائمة المواد الدراسية (مخزنة مؤقتاً)
subjects = ["اللغة العربية", "التربية الإسلامية"]

# --- القائمة الرئيسية ---
@bot.message_handler(commands=['start', 'admin'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    # إضافة أزرار المواد الموجودة
    for sub in subjects:
        markup.add(types.KeyboardButton(sub))
    
    # أزرار الإدارة لإضافة وحذف المواد
    add_btn = types.KeyboardButton("➕ إضافة مادة جديدة")
    del_btn = types.KeyboardButton("❌ حذف مادة")
    markup.add(add_btn, del_btn)
    
    bot.reply_to(message, "مرحباً بك! اختر المادة المطلوبة أو استخدم أزرار التحكم بالأسفل:", reply_markup=markup)

# --- عملية إضافة مادة جديدة ---
@bot.message_handler(func=lambda message: message.text == "➕ إضافة مادة جديدة")
def add_subject_prompt(message):
    msg = bot.send_message(message.chat.id, "أرسل الآن اسم المادة التي تريد إضافتها:")
    bot.register_next_step_handler(msg, process_add_subject)

def process_add_subject(message):
    new_sub = message.text
    if new_sub not in subjects:
        subjects.append(new_sub)
        bot.send_message(message.chat.id, f"✅ تم إضافة مادة **{new_sub}** بنجاح!")
    else:
        bot.send_message(message.chat.id, "⚠️ هذه المادة موجودة مسبقاً.")
    send_welcome(message)

# --- عملية حذف مادة ---
@bot.message_handler(func=lambda message: message.text == "❌ حذف مادة")
def delete_subject_prompt(message):
    msg = bot.send_message(message.chat.id, "أرسل اسم المادة التي تريد حذفها تماماً:")
    bot.register_next_step_handler(msg, process_delete_subject)

def process_delete_subject(message):
    sub_to_del = message.text
    if sub_to_del in subjects:
        subjects.remove(sub_to_del)
        bot.send_message(message.chat.id, f"🗑️ تم حذف مادة **{sub_to_del}**.")
    else:
        bot.send_message(message.chat.id, "❌ لم يتم العثور على مادة بهذا الاسم.")
    send_welcome(message)

# --- الأزرار الداخلية لكل مادة ---
@bot.message_handler(func=lambda message: message.text in subjects)
def show_subject_options(message):
    sub_name = message.text
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # تعريف الأزرار الأربعة لكل مادة بشكل آلي
    b1 = types.InlineKeyboardButton("📚 الكتاب والمنهج", callback_data=f"book_{sub_name}")
    b2 = types.InlineKeyboardButton("📅 خطة التدريس", callback_data=f"plan_{sub_name}")
    b3 = types.InlineKeyboardButton("📖 المكتبة", callback_data=f"lib_{sub_name}")
    b4 = types.InlineKeyboardButton("🏫 إدارة صفية", callback_data=f"admin_{sub_name}")
    
    markup.add(b1, b2, b3, b4)
    bot.send_message(message.chat.id, f"📂 ملفات مادة: **{sub_name}**", reply_markup=markup)

# --- التعامل مع ضغطات الأزرار الداخلية ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data.split('_')
    action = data[0]
    sub = data[1]
    
    response_text = ""
    if action == "book": response_text = f"جاري فتح كتاب {sub}..."
    elif action == "plan": response_text = f"جاري عرض خطة {sub}..."
    elif action == "lib": response_text = f"جاري فتح مكتبة {sub}..."
    elif action == "admin": response_text = f"جاري فتح نظام الإدارة لـ {sub}..."
    
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, response_text)

# تشغيل البوت باستمرار
bot.polling(none_stop=True)
