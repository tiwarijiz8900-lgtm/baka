import random
import asyncio
from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from baka.config import (
    PROTECT_1D_COST,
    PROTECT_2D_COST,
    REVIVE_COST,
    OWNER_ID
)

from baka.utils import (
    ensure_user_exists,
    resolve_target,
    get_active_protection,
    format_time,
    format_money,
    get_mention
)

from baka.database import users_collection


# =====================================================
# OPTIONAL GROQ IMPORT (safe)
# =====================================================
try:
    from baka.plugins.chatbot import ask_groq
except:
    ask_groq = None


# =====================================================
# ⚡ FAST NARRATOR (max 1 sec wait)
# =====================================================
async def get_narrative(action_type, attacker_mention, target_mention):
    if not ask_groq:
        return f"{attacker_mention} {action_type} {target_mention} 💀"

    prompt = (
        "Write very short funny kill message using P1 and P2."
        if action_type == "kill"
        else "Write very short robbery message using P1 and P2."
    )

    try:
        res = await asyncio.wait_for(ask_groq(prompt), timeout=1.2)
        if res and "P1" in res:
            return res.replace("P1", attacker_mention).replace("P2", target_mention)
    except:
        pass

    return f"{attacker_mention} {action_type} {target_mention} 💀"


# =====================================================
# 💀 KILL → DEAD
# =====================================================
async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    attacker = ensure_user_exists(update.effective_user)
    target, error = await resolve_target(update, context)

    if not target:
        return await update.message.reply_text("⚠️ Usage: /kill @user")

    if target.get('is_bot') or target['user_id'] == OWNER_ID:
        return await update.message.reply_text("🛡️ Protected user!")

    if attacker['status'] == 'dead' or target['status'] == 'dead':
        return await update.message.reply_text("💀 Dead user involved.")

    if target['user_id'] == attacker['user_id']:
        return await update.message.reply_text("🤦 Can't kill yourself.")

    expiry = get_active_protection(target)
    if expiry:
        rem = expiry - datetime.utcnow()
        return await update.message.reply_text(
            f"🛡️ Protected for {format_time(rem)}"
        )

    base_reward = random.randint(100, 200)

    weapons = [i for i in attacker.get('inventory', []) if i['type'] == 'weapon']
    buff = max([w['buff'] for w in weapons], default=0)

    final_reward = int(base_reward * (1 + buff))

    # fast db update
    users_collection.update_one(
        {"user_id": target["user_id"]},
        {"$set": {"status": "dead", "death_time": datetime.utcnow()}}
    )

    users_collection.update_one(
        {"user_id": attacker["user_id"]},
        {"$inc": {"kills": 1, "balance": final_reward}}
    )

    narration = await get_narrative(
        "kill",
        get_mention(attacker),
        get_mention(target)
    )

    # ✅ DEAD message
    await update.message.reply_text(
        f"💀 <b>DEAD!</b>\n\n"
        f"📝 <i>{narration}</i>\n\n"
        f"💵 Loot: <code>{format_money(final_reward)}</code>",
        parse_mode=ParseMode.HTML
    )


# =====================================================
# 💰 ROB
# =====================================================
async def rob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    attacker = ensure_user_exists(update.effective_user)

    if not context.args:
        return await update.message.reply_text("⚠️ /rob amount @user")

    try:
        amount = int(context.args[0])
    except:
        return await update.message.reply_text("⚠️ Invalid amount")

    target, error = await resolve_target(update, context)
    if not target:
        return await update.message.reply_text("Tag user")

    if target['balance'] < amount:
        return await update.message.reply_text("📉 Too poor")

    users_collection.update_one(
        {"user_id": target["user_id"]},
        {"$inc": {"balance": -amount}}
    )

    users_collection.update_one(
        {"user_id": attacker["user_id"]},
        {"$inc": {"balance": amount}}
    )

    narration = await get_narrative(
        "rob",
        get_mention(attacker),
        get_mention(target)
    )

    await update.message.reply_text(
        f"💰 <b>ROBBERY!</b>\n\n"
        f"📝 <i>{narration}</i>\n"
        f"💸 <code>{format_money(amount)}</code>",
        parse_mode=ParseMode.HTML
    )


# =====================================================
# 🛡️ PROTECT
# =====================================================
async def protect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = ensure_user_exists(update.effective_user)

    if not context.args:
        return await update.message.reply_text("⚠️ /protect 1d or 2d")

    dur = context.args[0]

    if dur == '1d':
        cost, days = PROTECT_1D_COST, 1
    elif dur == '2d':
        cost, days = PROTECT_2D_COST, 2
    else:
        return await update.message.reply_text("Only 1d or 2d")

    if sender['balance'] < cost:
        return await update.message.reply_text("❌ Not enough money")

    users_collection.update_one(
        {"user_id": sender["user_id"]},
        {"$inc": {"balance": -cost}}
    )

    expiry_dt = datetime.utcnow() + timedelta(days=days)

    users_collection.update_one(
        {"user_id": sender["user_id"]},
        {"$set": {"protection_expiry": expiry_dt}}
    )

    await update.message.reply_text("🛡️ Protection activated!")


# =====================================================
# ❤️ REVIVE
# =====================================================
async def revive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = ensure_user_exists(update.effective_user)

    if user['balance'] < REVIVE_COST:
        return await update.message.reply_text("❌ Not enough money")

    users_collection.update_one(
        {"user_id": user["user_id"]},
        {"$inc": {"balance": -REVIVE_COST}}
    )

    users_collection.update_one(
        {"user_id": user["user_id"]},
        {"$set": {"status": "alive"}}
    )

    await update.message.reply_text("💖 Revived!")
