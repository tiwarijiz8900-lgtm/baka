from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime, timedelta

# --- CONFIG ---
OWNER_ID = 123456789  # <--- Apni ID yahan dalye
MY_UPI_ID = "aapkaid@upi"

# Storage (Ise baad mein Database se connect karenge)
# { "user_id": {"plan": "monthly", "expiry": "2024-05-15"} }
PREMIUM_DATA = {}

async def premium_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={MY_UPI_ID}&am=99"
    text = (
        "🌟 **ANGEL PREMIUM PLANS** 🌟\n\n"
        "1️⃣ **Monthly:** ₹99 (30 Days)\n"
        "2️⃣ **Lifetime:** ₹999 (Forever)\n\n"
        "📌 **Process:** Payment karein aur niche di gayi command bhejien:\n"
        "`/apply_premium <TXN_ID> <monthly/lifetime>`"
    )
    await update.message.reply_photo(photo=qr_url, caption=text, parse_mode="Markdown")

async def apply_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if len(context.args) < 2:
        return await update.message.reply_text("❌ Format: `/apply_premium <TXN_ID> <plan>`")

    txn_id, plan = context.args[0], context.args[1].lower()
    
    keyboard = [[
        InlineKeyboardButton("✅ Approve", callback_data=f"prem_approve_{user.id}_{plan}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"prem_reject_{user.id}")
    ]]
    
    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=f"🔔 **NEW REQUEST**\n👤 {user.first_name}\n💰 Plan: {plan}\n🧾 TXN: {txn_id}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    await update.message.reply_text("✅ Request sent to Admin!")

async def premium_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data.split("_")
    await query.answer()

    if data[1] == "approve":
        user_id, plan = data[2], data[3]
        
        # Expiry Calculation
        days = 30 if plan == "monthly" else 36500 # 100 years for lifetime
        expiry_date = datetime.now() + timedelta(days=days)
        
        # Save to local memory (Ise DB mein save karna recommended hai)
        PREMIUM_DATA[user_id] = {
            "plan": plan,
            "expiry": expiry_date.strftime("%Y-%m-%d %H:%M:%S")
        }

        await context.bot.send_message(
            chat_id=int(user_id), 
            text=f"🎉 **Premium Activated!**\n📅 Plan: {plan.upper()}\n⌛ Expiry: {expiry_date.strftime('%d %b %Y')}"
        )
        await query.edit_message_text(f"✅ Approved user {user_id} for {plan}")

    elif data[1] == "reject":
        user_id = data[2]
        await context.bot.send_message(chat_id=int(user_id), text="❌ Your request was rejected.")
        await query.edit_message_text(f"❌ Rejected user {user_id}")

# Function to check if user is still premium
def is_premium(user_id):
    user_id = str(user_id)
    if user_id in PREMIUM_DATA:
        expiry = datetime.strptime(PREMIUM_DATA[user_id]["expiry"], "%Y-%m-%d %H:%M:%S")
        if datetime.now() < expiry:
            return True
        else:
            del PREMIUM_DATA[user_id] # Expired
    return False
