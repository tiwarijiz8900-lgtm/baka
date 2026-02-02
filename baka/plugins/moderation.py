from telegram import Update
from telegram.ext import ContextTypes

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    # Check if admin
    admin_check = await chat.get_member(user.id)
    if admin_check.status not in ['creator', 'administrator']:
        return await update.message.reply_text("❌ Sirf Admins hi kisi ko Ban kar sakte hain!")

    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Jis user ko ban karna hai, uske message pe reply karein.")

    target = update.message.reply_to_message.from_user
    try:
        await chat.ban_member(target.id)
        await update.message.reply_text(f"🚀 **BOOM!** {target.first_name} ko hamesha ke liye ban kar diya gaya! ✌️")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    admin_check = await chat.get_member(user.id)
    if admin_check.status not in ['creator', 'administrator']: return

    if not update.message.reply_to_message: return
    
    target = update.message.reply_to_message.from_user
    try:
        # User ko message bhejne se rokna
        from telegram import ChatPermissions
        permissions = ChatPermissions(can_send_messages=False)
        await chat.restrict_member(target.id, permissions)
        await update.message.reply_text(f"🤫 {target.first_name} ko Mute kar diya gaya hai. Ab shanti rahegi!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
