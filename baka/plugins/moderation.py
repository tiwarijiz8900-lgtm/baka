from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes


# ================= BAN =================
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    admin = await chat.get_member(user.id)
    if admin.status not in ["administrator", "creator"]:
        return await update.message.reply_text("❌ Only admins can ban.")

    if not update.message.reply_to_message:
        return await update.message.reply_text("Reply to user to ban.")

    target = update.message.reply_to_message.from_user

    await chat.ban_member(target.id)
    await update.message.reply_text(f"🔨 {target.first_name} banned permanently.")


# ================= MUTE =================
async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    admin = await chat.get_member(user.id)
    if admin.status not in ["administrator", "creator"]:
        return

    if not update.message.reply_to_message:
        return

    target = update.message.reply_to_message.from_user

    permissions = ChatPermissions(can_send_messages=False)
    await chat.restrict_member(target.id, permissions)

    await update.message.reply_text(f"🤫 {target.first_name} muted.")


# ================= UNMUTE =================
async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    admin = await chat.get_member(user.id)
    if admin.status not in ["administrator", "creator"]:
        return

    if not update.message.reply_to_message:
        return

    target = update.message.reply_to_message.from_user

    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True
    )

    await chat.restrict_member(target.id, permissions)

    await update.message.reply_text(f"✅ {target.first_name} unmuted.")


# ================= KICK =================
async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    admin = await chat.get_member(user.id)
    if admin.status not in ["administrator", "creator"]:
        return

    if not update.message.reply_to_message:
        return

    target = update.message.reply_to_message.from_user

    # kick = ban + unban instantly
    await chat.ban_member(target.id)
    await chat.unban_member(target.id)

    await update.message.reply_text(f"👢 {target.first_name} kicked from group.")
