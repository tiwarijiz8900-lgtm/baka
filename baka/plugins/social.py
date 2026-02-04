import random
import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatType

from baka.utils import (
    ensure_user_exists, resolve_target,
    get_mention, format_money, stylize_text
)

from baka.database import users_collection
from baka.config import DIVORCE_COST, BOT_NAME

# ✅ FIX → GROQ (safe)
try:
    from baka.plugins.chatbot import ask_groq
except:
    ask_groq = None


# =====================================================
# Helpers
# =====================================================

def get_progress_bar(percent):
    filled = int(percent / 10)
    return "█" * filled + "▒" * (10 - filled)


def get_love_comment(percent):
    if percent < 30: return "💔 Terrible!"
    if percent < 60: return "🤔 Hmm..."
    if percent < 90: return "💖 Good!"
    return "🔥 Soulmates!"


# =====================================================
# Couple Match
# =====================================================

async def couple_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    if chat.type == ChatType.PRIVATE:
        return await update.message.reply_text("❌ Group Only!")

    user1 = ensure_user_exists(user)

    target_arg = context.args[0] if context.args else None
    target, _ = await resolve_target(update, context, specific_arg=target_arg)

    if target:
        user2 = target
    else:
        pipeline = [
            {"$match": {"seen_groups": chat.id, "user_id": {"$ne": user.id}}},
            {"$sample": {"size": 1}}
        ]
        results = list(users_collection.aggregate(pipeline))
        if not results:
            return await update.message.reply_text("😔 No one else found.")
        user2 = results[0]

    percent = random.randint(0, 100)

    await update.message.reply_text(
        f"💘 <b>Match:</b> {get_mention(user1)} x {get_mention(user2)}\n"
        f"📊 <b>{percent}%</b> <code>{get_progress_bar(percent)}</code>\n"
        f"💭 <i>{get_love_comment(percent)}</i>",
        parse_mode=ParseMode.HTML
    )


# =====================================================
# Proposal
# =====================================================

async def propose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = ensure_user_exists(update.effective_user)

    if sender.get("partner_id"):
        return await update.message.reply_text("❌ Already married!")

    target, error = await resolve_target(update, context)
    if not target:
        return await update.message.reply_text(error or "⚠️ /propose @user")

    if target.get("partner_id"):
        return await update.message.reply_text("💔 Already taken.")

    s_id, t_id = sender['user_id'], target['user_id']

    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💍 Accept", callback_data=f"marry_y|{s_id}|{t_id}"),
            InlineKeyboardButton("🗑️ Reject", callback_data=f"marry_n|{s_id}|{t_id}")
        ]
    ])

    await update.message.reply_text(
        f"💘 <b>Proposal!</b>\n{get_mention(sender)} 💍 {get_mention(target)}",
        reply_markup=kb,
        parse_mode=ParseMode.HTML
    )


# =====================================================
# Divorce
# =====================================================

async def divorce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = ensure_user_exists(update.effective_user)

    if not user.get("partner_id"):
        return await update.message.reply_text("🤷‍♂️ Single.")

    if user['balance'] < DIVORCE_COST:
        return await update.message.reply_text(f"❌ Cost: {format_money(DIVORCE_COST)}")

    pid = user["partner_id"]

    users_collection.update_one(
        {"user_id": user["user_id"]},
        {"$set": {"partner_id": None}, "$inc": {"balance": -DIVORCE_COST}}
    )

    users_collection.update_one(
        {"user_id": pid},
        {"$set": {"partner_id": None}}
    )

    await update.message.reply_text("💔 Divorced!")


# =====================================================
# Callback
# =====================================================

async def proposal_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    action, p_id, t_id = query.data.split("|")

    p_id = int(p_id)
    t_id = int(t_id)

    if query.from_user.id != t_id:
        return await query.answer("Not for you", show_alert=True)

    if action == "marry_y":
        users_collection.update_one({"user_id": p_id}, {"$set": {"partner_id": t_id}})
        users_collection.update_one({"user_id": t_id}, {"$set": {"partner_id": p_id}})

        await query.message.edit_text("💍 Married ❤️")

    elif action == "marry_n":

        roast = "Rejected 😂"

        # ✅ GROQ roast (optional)
        if ask_groq:
            try:
                roast = await ask_groq("Roast a rejected proposal in funny Hindi.")
            except:
                pass

        await query.message.edit_text(
            f"❌ Rejected!\n🔥 {stylize_text(roast)}",
            parse_mode=ParseMode.HTML
        )
