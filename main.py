import telebot
from telebot import types

# التوكن الخاص بك مضاف هنا مباشرة
API_TOKEN = '8697358875:AAGaLUUDMR85ocFnM45yOUv-1iA6MXjcKyE'
bot = telebot.TeleBot(API_TOKEN)

# قائمة المواد الدراسية (تستطيع إضافتها وحذفها من البوت)
subjects = ["اللغة العربية", "التربية الإسلامية"]

@bot.message_handler(commands=['start', 'admin'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    # إضافة المواد الموجودة حالياً كأزرار كبيرة
    for sub in subjects:
        markup.add(types.KeyboardButton(sub))
    
    # أزرار التحكم للمدير (تظهر للكل حالياً لسهولة التجربة)
    admin_btn = types.KeyboardButton("➕ إضافة مادة جديدة")
    del_btn = types.KeyboardButton("❌ حذف مادة")
    markup.add(admin_btn, del_btn)
    
    bot.reply_to(message, "مرحباً بك! اختر المادة أو استخدم لوحة التحكم لإدارة البوت:", reply_markup=markup)

# --- قسم إضافة مادة جديدة ---
@bot.message_handler(func=lambda message: message.text == "➕ إضافة مادة جديدة")
def add_subject_prompt(message):
    msg = bot.send_message(message.chat.id, "أرسل اسم المادة التي تريد إضافتها (مثلاً: الرياضيات):")
    bot.register_next_step_handler(msg, process_add_subject)

def process_add_subject(message):
    new_sub = message.text
    if new_sub not in subjects:
        subjects.append(new_sub)
        bot.send_message(message.chat.id, f"✅ تم إضافة مادة **{new_sub}** بنجاح!")
    else:
        bot.send_message(message.chat.id, "⚠️ هذه المادة موجودة بالفعل.")
    send_welcome(message)

# --- قسم حذف مادة ---
@bot.message_handler(func=lambda message: message.text == "❌ حذف مادة")
def delete_subject_prompt(message):
    msg = bot.send_message(message.chat.id, "أرسل اسم المادة التي تريد حذفها بدقة:")
    bot.register_next_step_handler(msg, process_delete_subject)

def process_delete_subject(message):
    sub_to_del = message.text
    if sub_to_del in subjects:
        subjects.remove(sub_to_del)
        bot.send_message(message.chat.id, f"🗑️ تم حذف مادة **{sub_to_del}**.")
    else:
        bot.send_message(message.chat.id, "❌ لم أجد مادة بهذا الاسم.")
    send_welcome(message)

# --- قسم الأزرار الداخلية (داخل كل مادة) ---
@bot.message_handler(func=lambda message: message.text in subjects)
def show_subject_options(message):
    sub_name = message.text
    # إنشاء أزرار شفافة (تظهر تحت الرسالة)
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton("📚 الكتاب والمنهج", callback_data=f"book_{sub_name}")
    btn2 = types.InlineKeyboardButton("📅 خطة التدريس", callback_data=f"plan_{sub_name}")
    btn3 = types.InlineKeyboardButton("📖 المكتبة", callback_data=f"lib_{sub_name}")
    btn4 = types.InlineKeyboardButton("🏫 إدارة صفية", callback_data=f"admin_{sub_name}")
    
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, f"📂 قائمة خيارات مادة: **{sub_name}**", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # هنا نحدد ماذا يحدث عند الضغط على الأزرار الداخلية
    action = call.data.split('_')[0]
    sub = call.data.split('_')[1]
    
    messages = {
        "book": f"تحميل كتاب مادة {sub}...",
        "plan": f"عرض خطة تدريس مادة {sub}...",
        "lib": f"فتح مكتبة الوسائط لمادة {sub}...",
        "admin": f"نظام الإدارة الصفية لمادة {sub}..."
    }
    
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, messages.get(action, "جاري التحميل..."))

bot.polling(none_stop=True)
