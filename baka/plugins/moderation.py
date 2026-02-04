from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes


# ===============================
# COMMON ADMIN CHECK
# ===============================
async def is_admin(update: Update):
    user = update.effective_user
    chat = update.effective_chat

    member = await chat.get_member(user.id)
    return member.status in ["creator", "administrator"]


# ===============================
# BAN USER
# ===============================
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return await update.message.reply_text("❌ Sirf Admin hi ban kar sakte hain!")

    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply karo user pe ban karne ke liye.")

    target = update.message.reply_to_message.from_user

    try:
        await update.effective_chat.ban_member(target.id)
        await update.message.reply_text(
            f"🚫 {target.first_name} **BANNED FOREVER!** 💀"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


# ===============================
# MUTE USER
# ===============================
async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return

    if not update.message.reply_to_message:
        return

    target = update.message.reply_to_message.from_user

    try:
        permissions = ChatPermissions(can_send_messages=False)

        await update.effective_chat.restrict_member(target.id, permissions)

        await update.message.reply_text(
            f"🤫 {target.first_name} muted ho gaya!"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


# ===============================
# UNMUTE USER (🔥 FIX ADDED)
# ===============================
async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return

    if not update.message.reply_to_message:
        return

    target = update.message.reply_to_message.from_user

    try:
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )

        await update.effective_chat.restrict_member(target.id, permissions)

        await update.message.reply_text(
            f"✅ {target.first_name} unmuted ho gaya!"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


# ===============================
# KICK USER
# ===============================
async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return

    if not update.message.reply_to_message:
        return

    target = update.message.reply_to_message.from_user

    try:
        chat = update.effective_chat

        await chat.ban_member(target.id)
        await chat.unban_member(target.id)

        await update.message.reply_text(
            f"👢 {target.first_name} kicked out!"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
