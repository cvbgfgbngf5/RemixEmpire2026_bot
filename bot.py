import os
from dotenv import import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

load_dotenv()

# ==================== تنظیمات توکن ====================
TOKEN = "8896259846:AAHmFVAugdagw87BReMk6XG4Y0A76zb4ZYY"

# ==================== تنظیمات دو کانال ====================
CHANNEL_1_ID = "RemixEmpire2026"          # کانال اول (مثل کانال آموزشی)
CHANNEL_2_ID = "RemixEmpire2026"          # کانال دوم (مثل کانال ریمیکس)

# برای هر کانال یک متن و لینک جداگانه
channel_texts = {
    CHANNEL_1_ID: {
        "name": "آموزش و فروش کانفیک",
        "link_text": "لینک کانال آموزشی 👇",
        "link_url": "https://t.me/RemixEmpire2026",
        "verify_text": "عالی! حالا به امپراتوری خوش آمدید 🎧👑"
    },
    CHANNEL_2_ID: {
        "name": "امپراتوری ریمیکس",
        "link_text": "لینک کانال ریمیکس 👇",
        "link_url": "https://t.me/RemixEmpire2026",
        "verify_text": "عالی! حالا به امپراتوری خوش آمدید 🎧👑"
    }
}

SUPPORT_ID = "@Yilvf"

# Keyboard مرحله اول (دو دکمه)
btn1 = InlineKeyboardButton("آموزش و فروش کانفیک", callback_data="channel1")
btn2 = InlineKeyboardButton("امپراتوری ریمیکس", callback_data="channel2")
keyboard_step1 = InlineKeyboardMarkup([[btn1], [btn2]])

# Keyboard منوی اصلی (۴ دکمه در یک ردیف)
about_btn = InlineKeyboardButton("درباره ما", callback_data="about")
support_btn = InlineKeyboardButton("پشتیبانی", callback_data="support")
advertise_btn = InlineKeyboardButton("تبلیغات", callback_data="advertise")
keyboard_main_menu = InlineKeyboardMarkup([
    [about_btn, support_btn, advertise_btn]
])

# متن‌های خوشامدگویی
welcome_text = (
    "سلام به ربات **دانلود اینستاگرام** فرا** خوش آمدی ✨\n\n"
    "با من می‌تونی **ریپار، پست، عکس، ویدیو و استوری** اینستاگرام رو دانلود کنی\n\n"
    "برای استفاد از خدمات حتماً عضو دو کانال اسپانسر شو:\n"
    "1. آموزش و فروش کانفیک\n"
    "2. امپراتوری ریمیکس\n\n"
    "اول عضو شو، بعد روی «عضویت را تایید می‌کنم» بزن 🟢"
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
    f"{SUPPORT_ID}"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        welcome_text,
        reply_markup=keyboard_step1
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    user_id = query.from_user.id

    if query.data == "channel1":
        channel = CHANNEL_1_ID
        info = channel_texts[channel]
    elif query.data == "channel2":
        channel = CHANNEL_2_ID
        info = channel_texts[channel]
    else:
        return

    # پیام لینک مستقیم کانال (دقیقاً مثل نمونه عکس)
    channel_link = info["link_url"]
    await context.bot.send_message(
        chat_id,
        f"{info['link_text']}\n\n{channel_link}\n\n(کلیک کن و عضو شو 👑)",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("عضویت در کانال", url=channel_link)]])
    )

    # پیام بعد از عضویت
    await query.message.edit_text(
        f"🎉 <b>{info['name']}</b> عضویت در کانال موفقت‌آمیز!\n\n"
        "حالا می‌تونی از خدمات ربات استفاده کنی 👑\n\n"
        "برای عضویت در کانال روی دکمه زیر کلیک کن:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("عضویت در کانال", url=channel_link)]])
    )

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    chat_id = update.message.chat_id

    # چک عضویت در هر دو کانال
    all_member = True
    for ch_id in [CHANNEL_1_ID, CHANNEL_2_ID]:
        try:
            member = await context.bot.get_chat_member(ch_id, user.id)
            if member.status not in ["member", "administrator", "creator"]:
                all_member = False
                break
        except:
            all_member = False
            break

    if not all_member:
        await update.message.reply_text(
            "متأسفانه هنوز عضو هر دو کانال نیستی!\n"
            "لطفاً در هر دو کانال عضو شو و دوباره از /start بزن.",
            reply_markup=keyboard_step1
        )
    else:
        await update.message.reply_text(
            "عالی! حالا به امپراتوری خوش آمدید 🎧👑",
            reply_markup=keyboard_main_menu
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_membership))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
