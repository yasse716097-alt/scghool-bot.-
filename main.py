import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pymongo import MongoClient

# --- الإعدادات ---
# ضع التوكن الخاص بك هنا بين علامتي التنصيص
TOKEN = "8697358875:AAGaLUUDMR85ocFnM45yOUv-1iA6MXjcKyE"

# رابط قاعدة البيانات الخاص بك (تم تحديثه بكلمة المرور التي أرسلتها)
MONGO_URI = "mongodb+srv://Yasin:716097422@cluster0.0zr6uku.mongodb.net/?appName=Cluster0"

# الاتصال بقاعدة البيانات
client = MongoClient(MONGO_URI)
db = client['school_bot_db']
users_collection = db['users']

# إعداد السجلات (Logging)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- الوظائف ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # حفظ المستخدم في قاعدة البيانات إذا لم يكن موجوداً
    if not users_collection.find_one({"user_id": user.id}):
        users_collection.insert_one({
            "user_id": user.id,
            "username": user.username,
            "full_name": user.full_name
        })
    
    keyboard = [
        [InlineKeyboardButton("الكتب والمنهج 📚", callback_data='books')],
        [InlineKeyboardButton("خطة التدريس المقترحة 🗓️", callback_data='plan')],
        [InlineKeyboardButton("المكتبة 📖", callback_data='library')],
        [InlineKeyboardButton("الإدارة الصفية 🏫", callback_data='management')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"مرحباً بك يا {user.first_name} في بوت الإدارة المدرسية.\nالرجاء اختيار القسم المطلوب:",
        reply_markup=reply_markup
    )

# --- تشغيل البوت ---
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    print("البوت يعمل الآن...")
    application.run_polling()
