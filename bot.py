import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

load_dotenv()

# ==================== تنظیمات توکن ====================
TOKEN = "8896259846:AAHmFVAugdagw87BReMk6XG4Y0A76zb4ZYY"

# ==================== تنظیمات کانال و پشتیبانی ====================
CHANNEL_ID = "RemixEmpire2026"
SUPPORT_ID = "@Yilvf"

# Keyboard اصلی
channel_btn = InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/{CHANNEL_ID}")
about_btn = InlineKeyboardButton("درباره ما", callback_data="about")
support_btn = InlineKeyboardButton("پشتیبانی", callback_data="support")
advertise_btn = InlineKeyboardButton("تبلیغات", url=f"https://t.me/{SUPPORT_ID}")   # <--- دکمه تبلیغ جدید

keyboard = InlineKeyboardMarkup([
    [channel_btn, advertise_btn],
    [about_btn, support_btn]
])

# متن‌های خوشامدگویی (دقیقاً طبق خواسته‌ات)
welcome_text = (
    "به امپراتوری صدا خوش آمدید\n\n"
    "𝑹𝒆𝒆𝒎𝒊𝒙 𝑬𝒆𝒎𝒑𝒊𝒓𝒆 🎧👑\n\n"
    "بهترین ریمیکس‌های خاص منتظرتم 👑\n\n"
    "برای عضویت در کانال روی دکمه زیر کلیک کنید 👇"
)

about_text = (
    "𝑹𝒆𝒆𝒎𝒊𝒙 𝑬𝒆𝒎𝒑𝒊𝒓𝒆 🎧👑\n\n"
    "امپراتوری ریمیکس‌های خاص\n\n"
    "خلق ریمیکس‌های خلاقانه و باکیفیت\n\n"
    "برای طرفداران واقعی موسیقی\n\n"
    "هر روز نوآوری و انرژی\n\n"
    "به امپراتوری ما بپیوندید 👑"
)

support_text = (
    "𝑹𝒆𝒆𝒎𝒊𝒙 𝑬𝒆𝒎𝒑𝒊𝒓𝒆 🎧👑\n\n"
    "امپراتوری ریمیکس‌های خاص\n\n"
    "همه روزه ۲۴ ساعته آماده پاسخ به شما هستیم\n\n"
    "سوال، پیشنهاد یا هر کمکی لازم؟\n\n"
    "فوری کمکت می‌کنیم 👑\n\n"
    f"ایدی پشتیبانی : {SUPPORT_ID}"
)

advertise_text = (
    "برای هماهنگی و تبلیغات به ایدی زیر پیام دهید 👑\n\n"
    f"👑 پشتیبانی: {SUPPORT_ID}"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 👋\nبه امپراتوری ریمیکس خوش آمدید 🎧👑\n\n"
        "برای تجربه کامل، لطفاً در کانال عضو شوید.",
        reply_markup=keyboard
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "channel":
        await query.message.edit_text(
            "عالی! حالا برو تو کانال عضو شو 👑\n"
            "وقتی عضو شدی دوباره اینجا کلیک کن.",
            reply_markup=keyboard
        )
    elif query.data == "about":
        await query.message.edit_text(about_text, reply_markup=keyboard)
    elif query.data == "support":
        await query.message.edit_text(support_text, reply_markup=keyboard)
    elif query.data == "advertise":
        await query.message.edit_text(advertise_text, reply_markup=keyboard)

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    chat_member = await context.bot.get_chat_member(CHANNEL_ID, user.id)

    if chat_member.status not in ["member", "administrator", "creator"]:
        await update.message.reply_text(
            "متأسفانه هنوز عضو کانال نیستی!\n"
            "لطفاً در کانال عضو شو و دوباره از /start بزن.",
            reply_markup=keyboard
        )
    else:
        await update.message.reply_text("عالی! حالا به امپراتوری خوش آمدید 🎧👑", reply_markup=keyboard)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_membership))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
