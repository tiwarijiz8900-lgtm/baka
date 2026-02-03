# =========================================
# 💰 BAKA ECONOMY SYSTEM (FULL FIXED)
# =========================================

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from baka.database import users_collection
from baka.utils import (
    ensure_user_exists,
    get_mention,
    format_money,
    resolve_target
)

# =========================================
# ✅ CORE BALANCE FUNCTIONS (VERY IMPORTANT)
# =========================================

async def get_balance(user_id: int) -> int:
    """
    Returns user balance (used by battle/shop/give etc)
    """
    user = users_collection.find_one({"user_id": user_id})
    if not user:
        return 0
    return user.get("balance", 0)


async def update_balance(user_id: int, amount: int) -> int:
    """
    Add/Subtract money safely

    +amount = add
    -amount = remove
    """

    users_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"balance": amount}},
        upsert=True
    )

    user = users_collection.find_one({"user_id": user_id})
    return user.get("balance", 0)


# =========================================
# ✅ BALANCE COMMAND (/bal /balance)
# =========================================

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Shows wallet info
    """

    target, error = await resolve_target(update, context)

    if not target and error == "No target":
        target = ensure_user_exists(update.effective_user)
    elif not target:
        return await update.message.reply_text(error)

    bal = target.get("balance", 0)

    rank = users_collection.count_documents(
        {"balance": {"$gt": bal}}
    ) + 1

    kills = target.get("kills", 0)
    status = "💖 Alive" if target.get("status") == "alive" else "💀 Dead"

    text = (
        f"👤 <b>User:</b> {get_mention(target)}\n"
        f"👛 <b>Balance:</b> <code>{format_money(bal)}</code>\n"
        f"🏆 <b>Rank:</b> <code>#{rank}</code>\n"
        f"❤️ <b>Status:</b> {status}\n"
        f"⚔️ <b>Kills:</b> <code>{kills}</code>"
    )

    await update.message.reply_text(text, parse_mode=ParseMode.HTML)


# =========================================
# ✅ WRAPPER (FOR OLD PLUGINS LIKE COUPLE_BATTLE)
# =========================================

async def get_balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Some plugins import get_balance(update,context)
    so this wrapper avoids ImportError
    """
    return await balance(update, context)


# =========================================
# EXPORT SAFE NAMES
# =========================================

__all__ = [
    "get_balance",
    "update_balance",
    "balance",
    "get_balance_command"
]
