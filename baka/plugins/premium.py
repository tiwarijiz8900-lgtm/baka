from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from baka.config import OWNER_ID, UPI_ID, UPI_QR_IMAGE, PLAN_1_MONTH, PLAN_1_YEAR, PLAN_LIFETIME

async def premium_plans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show plans and UPI to user"""
    msg = (
        "🌟 **ᴀɴɢᴇʟ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴs** 🌟\n\n"
        f"◈ **1 Month** » ₹{PLAN_1_MONTH}\n"
        f"◈ **1 Year** » ₹{PLAN_1_YEAR}\n"
        f"◈ **Lifetime** » ₹{PLAN_LIFETIME}\n\n"
        f"💳 **ᴜᴘɪ ɪᴅ:** `{UPI_ID}`\n\n"
        "📝 **ʜᴏᴡ ᴛᴏ ʙᴜʏ:**\n"
        "1. Upar di gayi UPI par payment karein.\n"
        "2. Screenshot lekar @ll_WTF_SHEZADA_ll ko bhejein.\n"
        "3. Verification ke baad aapka premium active ho jayega!"
    )
    await update.message.reply_photo(photo=UPI_QR_IMAGE, caption=msg, parse_mode="Markdown")

async def approve_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin approves user subscription by replying to their message"""
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("❌ Only Owner can approve!")

    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to user's proof with `/approve <months>`")

    if not context.args:
        return await update.message.reply_text("⚠️ Specify months! (e.g. `/approve 1` or `/approve 12`)")

    months = int(context.args[0])
    target = update.message.reply_to_message.from_user
    
    # Expiry calculation logic
    expiry_date = datetime.now() + timedelta(days=30 * months)
    expiry_str = expiry_date.strftime('%d-%m-%Y')

    # Note: Replace with your DB update logic (e.g. users_collection.update_one)
    await update.message.reply_text(
        f"✅ **ᴘʀᴇᴍɪᴜᴍ ᴀᴘᴘʀᴏᴠᴇᴅ!**\n\n"
        f"👤 **ᴜsᴇʀ:** {target.first_name}\n"
        f"⏳ **ᴅᴜʀᴀᴛɪᴏɴ:** {months} Month(s)\n"
        f"📅 **ᴇxᴘɪʀʏ:** `{expiry_str}`"
    )
