from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# --- CONFIG ---
OWNER_ID = 123456789  # <--- APNI TELEGRAM ID YAHAN DALO
MY_UPI_ID = "yourid@upi"

async def premium_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={MY_UPI_ID}&am=99"
    
    text = (
        "🌟 **ANGEL PREMIUM PLANS** 🌟\n\n"
        "1️⃣ **Monthly:** ₹99\n"
        "2️⃣ **Lifetime:** ₹999\n\n"
        "📌 **Kaise lein?**\n"
        "QR Scan karke payment karein aur niche di gayi command use karein:\n"
        "`/apply_premium <Transaction_ID> <Plan_Type>`\n\n"
        "Example: `/apply_premium TXN12345 lifetime`"
    )
    await update.message.reply_photo(photo=qr_url, caption=text, parse_mode="Markdown")

# User request bhejega
async def apply_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not context.args or len(context.args) < 2:
        return await update.message.reply_text("❌ Format: `/apply_premium <TXN_ID> <monthly/lifetime>`")

    txn_id = context.args[0]
    plan = context.args[1]

    # Admin ko approval message bhejna
    keyboard = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"prem_approve_{user.id}_{plan}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"prem_reject_{user.id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=f"🔔 **NEW PREMIUM REQUEST**\n\n"
             f"👤 User: {user.first_name} (@{user.username})\n"
             f"🆔 ID: `{user.id}`\n"
             f"💰 Plan: {plan.upper()}\n"
             f"🧾 TXN ID: `{txn_id}`",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    await update.message.reply_text("✅ Aapki request Admin ko bhej di gayi hai. Approval ka intezar karein! 😘")

# Button Click Handle karna
async def premium_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data.startswith("prem_approve_"):
        _, _, user_id, plan = data.split("_")
        # Yahan Database me save karne ka logic aayega (Jaise maine pehle bataya tha)
        
        await context.bot.send_message(chat_id=int(user_id), text=f"🎉 Mubarak ho! Aapka **{plan.upper()}** Premium Approve ho gaya hai!")
        await query.edit_message_text(f"✅ User `{user_id}` approved for {plan}!")

    elif data.startswith("prem_reject_"):
        user_id = data.split("_")[2]
        await context.bot.send_message(chat_id=int(user_id), text="❌ Sorry! Aapki Premium request reject kar di gayi hai. Support se baat karein.")
        await query.edit_message_text(f"❌ User `{user_id}` rejected.")
