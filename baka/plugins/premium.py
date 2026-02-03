# Copyright (c) 2025 Telegram:- @WTF_Phantom <DevixOP>

from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes

from baka.config import (
    OWNER_ID,
    UPI_ID,
    UPI_QR_IMAGE,
    PLAN_1_MONTH,
    PLAN_1_YEAR,
    PLAN_LIFETIME
)

from baka.database import users_collection, add_premium_user


# ======================================================
# ✅ IMPORTANT FUNCTION (FIX FOR ALL PLUGINS)
# ======================================================
# ⚠️ Ye function missing tha → isi wajah se Heroku crash ho raha tha

def is_premium(user_id: int) -> bool:
    """Check if user has active premium"""

    user = users_collection.find_one({"user_id": user_id})

    if not user:
        return False

    if not user.get("is_premium"):
        return False

    expiry = user.get("premium_expiry")

    # Lifetime
    if not expiry:
        return True

    # Expired check
    if expiry < datetime.now():
        users_collection.update_one(
            {"user_id": user_id},
            {"$set": {"is_premium": False}}
        )
        return False

    return True


# ======================================================
# 🌟 USER COMMANDS
# ======================================================

async def premium_plans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows plans + QR"""

    msg = (
        "🌟 **ᴀɴɢᴇʟ ᴘʀᴇᴍɪᴜᴍ sᴇʀᴠɪᴄᴇs** 🌟\n\n"
        "👑 **ᴇxᴄʟᴜsɪᴠᴇ ᴘʟᴀɴs:**\n"
        f"◈ 1 Month  » ₹{PLAN_1_MONTH}\n"
        f"◈ 1 Year   » ₹{PLAN_1_YEAR}\n"
        f"◈ Lifetime » ₹{PLAN_LIFETIME}\n\n"
        f"💳 **UPI ID:** `{UPI_ID}`\n\n"
        "Screenshot bhejo owner ko for activation."
    )

    try:
        await update.message.reply_photo(
            photo=UPI_QR_IMAGE,
            caption=msg,
            parse_mode="Markdown"
        )
    except:
        await update.message.reply_text(msg, parse_mode="Markdown")


async def check_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User checks their premium"""

    user_id = update.effective_user.id
    name = update.effective_user.first_name

    user = users_collection.find_one({"user_id": user_id})

    if not user or not user.get("is_premium"):
        return await update.message.reply_text(
            f"❌ {name}, aap premium nahi ho."
        )

    expiry = user.get("premium_expiry")

    if expiry and expiry.year >= 2090:
        expiry_str = "Lifetime ♾️"
        days_left = "Unlimited"
    else:
        expiry_str = expiry.strftime("%d-%m-%Y")
        days_left = (expiry - datetime.now()).days

    await update.message.reply_text(
        f"🌟 **Premium Status**\n\n"
        f"👤 User: {name}\n"
        f"📅 Expiry: `{expiry_str}`\n"
        f"⏳ Remaining: {days_left} days",
        parse_mode="Markdown"
    )


# ======================================================
# ⚙️ ADMIN COMMANDS (OWNER ONLY)
# ======================================================

async def approve_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reply + /approve 1 or 12 or 999"""

    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("❌ Only Owner allowed!")

    if not update.message.reply_to_message:
        return await update.message.reply_text(
            "Reply user + /approve <months>"
        )

    if not context.args:
        return await update.message.reply_text("Example: /approve 1")

    try:
        months = int(context.args[0])
        target = update.message.reply_to_message.from_user

        expiry_date = add_premium_user(target.id, months)

        expiry_str = (
            "Lifetime ♾️"
            if months >= 999
            else expiry_date.strftime("%d-%m-%Y")
        )

        await update.message.reply_text(
            f"✅ Premium Activated!\n\n"
            f"User: {target.first_name}\n"
            f"Expiry: {expiry_str}"
        )

        try:
            await context.bot.send_message(
                target.id,
                "🎉 Your Premium is active!"
            )
        except:
            pass

    except:
        await update.message.reply_text("Invalid number")


async def remove_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reply + /unpremium"""

    if update.effective_user.id != OWNER_ID:
        return

    if not update.message.reply_to_message:
        return

    target = update.message.reply_to_message.from_user

    users_collection.update_one(
        {"user_id": target.id},
        {"$set": {"is_premium": False, "premium_expiry": None}}
    )

    await update.message.reply_text(
        f"🚫 Premium removed for {target.first_name}"
    )
