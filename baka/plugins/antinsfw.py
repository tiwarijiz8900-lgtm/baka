from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

# ===============================
# SETTINGS (memory based)
# ===============================
NSFW_STATUS = {}   # chat_id : True/False


# ===============================
# BAD WORDS / LINKS
# ===============================
BAD_WORDS = [
    "porn", "sex", "xxx", "nude", "boobs",
    "fuck", "hentai", "adult", "18+", "naked"
]

BAD_LINKS = [
    "pornhub", "xnxx", "xvideos", "redtube", "rule34"
]


# ===============================
# ADMIN CHECK
# ===============================
async def is_admin(chat, user_id):
    member = await chat.get_member(user_id)
    return member.status in ["administrator", "creator"]


# ===============================
# /nsfw ON OFF COMMAND
# ===============================
async def nsfw_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat = update.effective_chat
    user = update.effective_user

    # only admin allowed
    if not await is_admin(chat, user.id):
        return await update.message.reply_text("❌ Sirf admins hi use kar sakte hain!")

    if not context.args:
        return await update.message.reply_text("Use:\n/nsfw on\n/nsfw off")

    arg = context.args[0].lower()

    if arg == "on":
        NSFW_STATUS[chat.id] = True
        await update.message.reply_text("✅ NSFW Protection Enabled 🔥")

    elif arg == "off":
        NSFW_STATUS[chat.id] = False
        await update.message.reply_text("❌ NSFW Protection Disabled")

    else:
        await update.message.reply_text("Use only: on / off")


# ===============================
# MAIN GUARD
# ===============================
async def nsfw_guard(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = update.message
    if not msg:
        return

    chat = update.effective_chat
    user = update.effective_user

    # check enabled
    if not NSFW_STATUS.get(chat.id, False):
        return

    # ignore admins
    if await is_admin(chat, user.id):
        return

    text = (msg.text or msg.caption or "").lower()

    detected = False

    # 🔴 words
    for w in BAD_WORDS:
        if w in text:
            detected = True

    # 🔴 links
    for l in BAD_LINKS:
        if l in text:
            detected = True

    # 🔴 media auto delete
    if (
        msg.photo or
        msg.video or
        msg.animation or
        msg.sticker or
        msg.document or
        msg.voice
    ):
        detected = True

    if not detected:
        return

    try:
        await msg.delete()

        # mute 5 minutes
        perms = ChatPermissions(can_send_messages=False)
        await chat.restrict_member(user.id, perms)

        await context.bot.send_message(
            chat.id,
            f"🔞 {user.first_name} NSFW/Media not allowed!\n🤫 5 min mute."
        )

    except:
        pass
