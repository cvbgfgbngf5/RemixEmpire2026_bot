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

# Keyboard اصلی (دقیقاً ۴ دکمه کاملاً در ردیف‌های جدا - هر دکمه روی یک خط)
channel_btn = InlineKeyboardButton("𝑹𝒆𝒆𝒎𝒙 𝑬𝒆𝒆𝒎𝒑𝒊𝒓𝒆 🎧👑 | امپراتوری ریمیکس", url="https://t.me/RemixEmpire2026")
check_btn = InlineKeyboardButton("تایید عضویت", callback_data="check")
about_btn = InlineKeyboardButton("درباره ما", callback_data="about")
support_btn = InlineKeyboardButton("پشتیبانی", callback_data="support")

keyboard = InlineKeyboardMarkup([
    [channel_btn],
    [check_btn],
    [about_btn],
    [support_btn]
])

# متن شروع ربات
start_text = (
    "سلام! 👋\nبه امپراتوری ریمیکس خوش آمدید 🎧👑\n\n"
    "برای تجربه کامل، لطفاً در کانال عضو شوید."
)

# متن‌های خوشامدگویی (دقیقاً طبق خواسته‌ت)
welcome_text = (
    "به امپراتوری صدا خوش آمدید\n\n"
    "𝑹𝒆𝒆𝒎𝒙 𝑬𝒆𝒆𝒎𝒑𝒊𝒓𝒆 🎧👑\n\n"
    "بهترین ریمیکس‌های خاص منتظرتم 👑\n\n"
    "برای عضویت در کانال روی دکمه زیر کلیک کنید 👇"
)

about_text = (
    "𝑹𝒆𝒆𝒎𝒙 𝑬𝒆𝒆𝒎𝒑𝒊𝒓𝒆 🎧👑\n\n"
    "امپراتوری ریمیکس‌های خاص\n\n"
    "خلق ریمیکس‌های خلاقانه و باکیفیت\n\n"
    "برای طرفداران واقعی موسیقی\n\n"
    "هر روز نوآوری و انرژی\n\n"
    "به امپراتوری ما بپیوندید 👑"
)

support_text = (
    "𝑹𝒆𝒆𝒎𝒙 𝑬𝒆𝒆𝒆𝒎𝒑𝒊𝒓𝒆 🎧👑\n\n"
    "امپراتوری ریمیکس‌های خاص\n\n"
    "همه روزه ۲۴ ساعته آماده پاسخ به شما هستیم\n\n"
    "سوال، پیشنهاد یا هر کمکی لازم؟\n\n"
    "فوری کمکت می‌کنیم 👑\n\n"
    f"ایدی پشتیبانی : {SUPPORT_ID}"
)

advertise_text = (
    "برای هماهنگی و تبلیغات به ایدی زیر پیام دهید 👑\n\n"
    f"{SUPPORT_ID}"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        start_text,
        reply_markup=keyboard
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about":
        await query.message.edit_text(about_text, reply_markup=keyboard)
    elif query.data == "support":
        await query.message.edit_text(support_text, reply_markup=keyboard)
    elif query.data == "advertise":
        await query.message.edit_text(advertise_text, reply_markup=keyboard)
    elif query.data == "check":
        await check_membership(update, context)


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
        # ✅ متن خوشامدگویی دقیقاً همان متن اصلی
        welcome_text = (
            "به امپراتوری صدا خوش آمدید\n\n"
            "𝑹𝒆𝒆𝒎𝒙 𝑬𝒆𝒆𝒆𝒎𝒑𝒊𝒓𝒆 🎧👑\n\n"
            "بهترین ریمیکس‌های خاص منتظرتم 👑\n\n"
            "برای عضویت در کانال روی دکمه زیر کلیک کنید 👇"
        )

        # Keyboard برای بعد از عضویت (دقیقاً همان ۴ دکمه اصلی)
        service_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("𝑹𝒆𝒆𝒎𝒙 𝑬𝒆𝒆𝒆𝒎𝒑𝒊𝒓𝒆 🎧👑 | امپراتوری ریمیکس", url="https://t.me/RemixEmpire2026")],
            [InlineKeyboardButton("تایید عضویت", callback_data="check")],
            [InlineKeyboardButton("درباره ما", callback_data="about")],
            [InlineKeyboardButton("پشتیبانی", callback_data="support")]
        ])

        await update.message.reply_text(
            welcome_text,
            reply_markup=service_keyboard
        )


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_membership))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
