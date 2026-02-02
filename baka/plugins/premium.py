from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from baka.config import OWNER_ID, UPI_ID, UPI_QR_IMAGE, PLAN_1_MONTH, PLAN_1_YEAR, PLAN_LIFETIME
from baka.database import users_collection, add_premium_user # Database functions

# ======================================================
# 🌟 USER COMMANDS
# ======================================================

async def premium_plans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Users ko plans aur UPI QR dikhata hai."""
    msg = (
        "🌟 **ᴀɴɢᴇʟ ᴘʀᴇᴍɪᴜᴍ sᴇʀᴠɪᴄᴇs** 🌟\n\n"
        "👑 **ᴇxᴄʟᴜsɪᴠᴇ ᴘʟᴀɴs:**\n"
        f"◈ 1 Month  » ₹{PLAN_1_MONTH}\n"
        f"◈ 1 Year   » ₹{PLAN_1_YEAR}\n"
        f"◈ Lifetime » ₹{PLAN_LIFETIME}\n\n"
        f"💳 **ᴜᴘɪ ɪᴅ:** `{UPI_ID}`\n\n"
        "📝 **ʜᴏᴡ ᴛᴏ ʙᴜʏ:**\n"
        "1. Upar di gayi UPI par payment karein.\n"
        "2. Screenshot lekar @ll_WTF_ZEXX_ll ko bhejein.\n"
        "3. Verification ke baad aapka premium active ho jayega!"
    )
    try:
        await update.message.reply_photo(photo=UPI_QR_IMAGE, caption=msg, parse_mode="Markdown")
    except Exception:
        await update.message.reply_text(msg, parse_mode="Markdown")

async def check_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User apni subscription validity check karta hai."""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    user_data = users_collection.find_one({"user_id": user_id})
    
    if not user_data or not user_data.get("is_premium"):
        return await update.message.reply_text(f"❌ **{user_name}**, aapke paas koi active premium plan nahi hai.")

    expiry = user_data.get("premium_expiry")
    
    # Lifetime check
    if expiry and expiry.year >= 2090:
        expiry_str = "Lifetime ♾️"
        days_left = "Unlimited"
    else:
        expiry_str = expiry.strftime('%d-%m-%Y')
        days_left = (expiry - datetime.now()).days

    await update.message.reply_text(
        f"🌟 **ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ sᴛᴀᴛᴜs** 🌟\n\n"
        f"👤 **ᴜsᴇʀ:** {user_name}\n"
        f"📅 **ᴇxᴘɪʀʏ:** `{expiry_str}`\n"
        f"⏳ **ʀᴇᴍᴀɪɴɪɴɢ:** {days_left} Days\n\n"
        "Thank you for being part of Angel Elite! 🌸"
    )

# ======================================================
# ⚙️ ADMIN COMMANDS (OWNER ONLY)
# ======================================================

async def approve_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin user ke message pe reply karke premium active karta hai."""
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("❌ Sirf Boss hi approve kar sakte hain!")

    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ User ke screenshot par reply karein: `/approve <months>`\n(Lifetime ke liye 999 likhein)")

    if not context.args:
        return await update.message.reply_text("⚠️ Kitne mahine? `/approve 1` ya `/approve 12` likhein.")

    try:
        months = int(context.args[0])
        target = update.message.reply_to_message.from_user
        
        # Database Update
        expiry_date = add_premium_user(target.id, months)
        
        expiry_str = "Lifetime ♾️" if months >= 999 else expiry_date.strftime('%d-%m-%Y')

        await update.message.reply_text(
            f"✅ **ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴛɪᴠᴀᴛᴇᴅ!**\n\n"
            f"👤 **ᴜsᴇʀ:** {target.first_name}\n"
            f"🆔 **ɪᴅ:** `{target.id}`\n"
            f"⏳ **ᴅᴜʀᴀᴛɪᴏɴ:** {months} Month(s)\n"
            f"📅 **ᴇxᴘɪʀʏ:** `{expiry_str}`\n\n"
            f"Ab {target.first_name} bot ke saare exclusive features use kar sakta hai! 🚀"
        )
        
        # User ko notify karna
        try:
            await context.bot.send_message(
                chat_id=target.id,
                text=f"🎊 **Congratulations!**\nAapka Premium Plan ({months} months) active ho gaya hai!\nAb maza lo! 🌸"
            )
        except:
            pass

    except ValueError:
        await update.message.reply_text("❌ Months sirf numbers mein likhein (e.g. 1, 6, 12)")

async def remove_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin premium access chin sakta hai."""
    if update.effective_user.id != OWNER_ID:
        return 
    
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ User ke message pe reply karke `/unpremium` likhein.")

    target = update.message.reply_to_message.from_user
    users_collection.update_one({"user_id": target.id}, {"$set": {"is_premium": False, "premium_expiry": None}})
    
    await update.message.reply_text(f"🚫 Premium access removed for {target.first_name}.")
