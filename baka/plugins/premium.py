from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from baka.config import MONGO_URL # Ensure this is in your config
import motor.motor_asyncio

# --- MONGODB SETUP ---
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client["angel_bot_db"]
premium_db = db["premium_users"]

# --- CONFIG ---
OWNER_ID = 123456789  # <--- Apni ID dalo
MY_UPI_ID = "aapkaid@upi"

async def premium_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={MY_UPI_ID}&am=99"
    text = (
        "🌟 **ANGEL PREMIUM PLANS** 🌟\n\n"
        "1️⃣ **Monthly:** ₹99 (30 Days)\n"
        "2️⃣ **Lifetime:** ₹999 (Forever)\n\n"
        "📌 **Process:** Payment karein aur niche di gayi command bhejien:\n"
        "`/apply_premium <TXN_ID> <plan>`\n\n"
        "Angel aapka wait kar rahi hai! 😘"
    )
    await update.message.reply_photo(photo=qr_url, caption=text, parse_mode="Markdown")

async def apply_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if len(context.args) < 2:
        return await update.message.reply_text("❌ Format: `/apply_premium <TXN_ID> <monthly/lifetime>`")

    txn_id, plan = context.args[0], context.args[1].lower()
    
    keyboard = [[
        InlineKeyboardButton("✅ Approve", callback_data=f"prem_approve_{user.id}_{plan}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"prem_reject_{user.id}")
    ]]
    
    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=f"🔔 **NEW PREMIUM REQUEST**\n👤 {user.first_name}\n💰 Plan: {plan}\n🧾 TXN: {txn_id}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    await update.message.reply_text("✅ Request Admin ko bhej di gayi hai! Approval ka wait karein. ✨")

async def premium_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data.split("_")
    await query.answer()

    if data[1] == "approve":
        user_id = int(data[2])
        plan = data[3]
        
        # Expiry Logic
        days = 30 if plan == "monthly" else 36500 
        expiry_date = datetime.now() + timedelta(days=days)
        
        # MongoDB mein Save/Update karna
        await premium_db.update_one(
            {"user_id": user_id},
            {"$set": {"plan": plan, "expiry": expiry_date}},
            upsert=True
        )

        await context.bot.send_message(
            chat_id=user_id, 
            text=f"🎉 **Premium Activated!**\n📅 Plan: {plan.upper()}\n⌛ Expiry: {expiry_date.strftime('%d %b %Y')}\n\nAb aap Angel ke VIP hain! ❤️"
        )
        await query.edit_message_text(f"✅ Approved user {user_id} for {plan}")

    elif data[1] == "reject":
        user_id = int(data[2])
        await context.bot.send_message(chat_id=user_id, text="❌ Sorry! Admin ne aapki premium request reject kar di hai.")
        await query.edit_message_text(f"❌ Rejected user {user_id}")

# --- Helper Function to check Premium (Everywhere) ---
async def is_premium(user_id):
    user = await premium_db.find_one({"user_id": int(user_id)})
    if user:
        if datetime.now() < user["expiry"]:
            return True
        else:
            await premium_db.delete_one({"user_id": int(user_id)}) # Auto delete if expired
    return False
