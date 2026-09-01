import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

load_dotenv()

# ==================== تنظیمات ====================
TOKEN = "8896259846:AAHmFVAugdagw87BReMk6XG4Y0A76zb4ZYY"
CHANNEL_ID = "RemixEmpire2026"
SUPPORT_ID = "@Yilvf"

# Keyboard اصلی (استایل شاهانه)
channel_btn = InlineKeyboardButton("🔗 عضویت در کانال", url=f"https://t.me/{CHANNEL_ID}")
about_btn = InlineKeyboardButton("📖 درباره ما", callback_data="about")
support_btn = InlineKeyboardButton("🤝 پشتیبانی", callback_data="support")
advertise_btn = InlineKeyboardButton("💎 تبلیغات", url=f"https://t.me/{SUPPORT_ID.lstrip('@')}")

keyboard = InlineKeyboardMarkup([
    [channel_btn, advertise_btn],
    [about_btn, support_btn]
])

# ==================== متن‌های پریمیوم ====================
welcome_text = (
    "به امپراتوری صدا خوش آمدید ✨\n\n"
    "𝑹𝒆𝒆𝒎𝒊𝒙 𝑬𝒆𝒎𝒑𝒊𝒓𝒆 🎧👑\n\n"
    "بهترین ریمیکس‌های خاص جهان منتظرتم 💎\n\n"
    "هر روز نوآوری 🔥\n\n"
    "برای عضویت در کانال روی دکمه زیر کلیک کنید 👇"
)

about_text = (
    "𝑹𝒆𝒆𝒎𝒊𝒙 𝑬𝒆𝒎𝒑𝒊𝒓𝒆 🎧👑\n\n"
    "امپراتوری ریمیکس‌های خاص ✨\n\n"
    "خلق ریمیکس‌های خلاقانه و باکیفیت 💎\n\n"
    "برای طرفداران واقعی موسیقی 👑\n\n"
    "هر روز نوآوری و انرژی 🔥\n\n"
    "به امپراتوری ما بپیوندید 👑"
)

support_text = (
    "𝑹𝒆𝒆𝒎𝒊𝒙 𝑬𝒆𝒎𝒑𝒊𝒓𝒆 🎧👑\n\n"
    "امپراتوری ریمیکس‌های خاص ✨\n\n"
    "همه روزه ۲۴ ساعته آماده پاسخ به شما هستیم 💎\n\n"
    "سوال، پیشنهاد یا هر کمکی لازم؟\n\n"
    "فوری کمکت می‌کنیم 👑\n\n"
    f"ایدی پشتیبانی : {SUPPORT_ID}"
)

advertise_text = (
    "برای هماهنگی و تبلیغات به ایدی زیر پیام دهید 👑\n\n"
    f"👑 پشتیبانی: {SUPPORT_ID}"
)

# ==================== هندلرهای جدید (کابوم متحرک) ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # === کابوم متحرک شاهانه ===
    await update.message.reply_text(
        "🎉🎆💥 𝙆𝘼𝘽𝙊𝙊𝙈! 𝙎𝙤𝙪𝙣𝙙 𝙀𝙢𝙥𝙞𝙧𝙚 𝙎𝙩𝙖𝙧𝙩𝙚𝙙! 💥🎆🎉\n\n"
        "به امپراتوری ریمیکس خوش آمدید ✨\n\n"
        "هر روز نوآوری 🔥\n\n"
        "برای عضویت در کانال روی دکمه زیر کلیک کنید 👇",
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
        link = f"https://t.me/{SUPPORT_ID.lstrip('@')}"
        await query.message.edit_text(
            f"پشتیبانی رو باز کن 👑\n\n{link}\n\nبرای ارتباط فوری:",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔗 باز کردن پشتیبانی", url=link)
            ]])
        )
    elif query.data == "advertise":
        await query.message.edit_text(advertise_text, reply_markup=keyboard)

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await context.bot.get_chat_member(CHANNEL_ID, update.message.from_user.id).status in ["member", "administrator", "creator"]:
        await update.message.reply_text("عالی! حالا به امپراتوری خوش آمدید 🎧👑", reply_markup=keyboard)
    else:
        await update.message.reply_text("متأسفانه هنوز عضو کانال نیستی!\nلطفاً در کانال عضو شو و دوباره از /start بزن.", reply_markup=keyboard)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_membership))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
