import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from baka.config import PROTECT_1D_COST, PROTECT_2D_COST, REVIVE_COST, AUTO_REVIVE_HOURS, OWNER_ID
from baka.utils import (
    ensure_user_exists, resolve_target, is_protected, get_active_protection,
    format_time, format_money, get_mention, check_auto_revive
)
from baka.database import users_collection

# ✅ FIXED → GROQ use karenge (Mistral hata diya)
try:
    from baka.plugins.chatbot import ask_groq
except:
    ask_groq = None


# =====================================================
# ✅ AI NARRATOR (SAFE + GROQ)
# =====================================================

async def get_narrative(action_type, attacker_mention, target_mention):
    if action_type == 'kill':
        prompt = "Write a short funny game kill message using P1 and P2."
    elif action_type == 'rob':
        prompt = "Write a short funny robbery message using P1 and P2."
    else:
        return f"{attacker_mention} -> {target_mention}"

    res = None

    # GROQ call (safe)
    if ask_groq:
        try:
            res = await ask_groq(prompt)
        except:
            res = None

    text = res if res and "P1" in str(res) else f"P1 {action_type} P2!"

    return text.replace("P1", attacker_mention).replace("P2", target_mention)


# =====================================================
# 🔪 KILL
# =====================================================

async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    attacker = ensure_user_exists(update.effective_user)
    target, error = await resolve_target(update, context)

    if not target:
        return await update.message.reply_text(
            error or "⚠️ <b>Usage:</b> <code>/kill @user</code>",
            parse_mode=ParseMode.HTML
        )

    if target.get('is_bot') or target['user_id'] == OWNER_ID:
        return await update.message.reply_text("🛡️ Protected!", parse_mode=ParseMode.HTML)

    if attacker['status'] == 'dead' or target['status'] == 'dead':
        return await update.message.reply_text("💀 Dead user involved.", parse_mode=ParseMode.HTML)

    if target['user_id'] == attacker['user_id']:
        return await update.message.reply_text("🤦‍♂️ No self kill.", parse_mode=ParseMode.HTML)

    expiry = get_active_protection(target)
    if expiry:
        rem = expiry - datetime.utcnow()
        return await update.message.reply_text(
            f"🛡️ Safe for <code>{format_time(rem)}</code>",
            parse_mode=ParseMode.HTML
        )

    base_reward = random.randint(100, 200)

    weapons = [i for i in attacker.get('inventory', []) if i['type'] == 'weapon']
    best_w = max(weapons, key=lambda x: x['buff']) if weapons else None
    buff = best_w['buff'] if best_w else 0

    final_reward = int(base_reward * (1 + buff))

    users_collection.update_one(
        {"user_id": target["user_id"]},
        {"$set": {"status": "dead", "death_time": datetime.utcnow()}}
    )

    users_collection.update_one(
        {"user_id": attacker["user_id"]},
        {"$inc": {"kills": 1, "balance": final_reward}}
    )

    narration = await get_narrative("kill", get_mention(attacker), get_mention(target))

    await update.message.reply_text(
        f"🔪 <b>MURDER!</b>\n\n{i
mplementation error?}
📝 <i>{narration}</i>\n\n💵 Loot: <code>{format_money(final_reward)}</code>",
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
        return await update.message.reply_text(error or "Tag user")

    if target['balance'] < amount:
        return await update.message.reply_text("📉 Too poor")

    users_collection.update_one({"user_id": target["user_id"]}, {"$inc": {"balance": -amount}})
    users_collection.update_one({"user_id": attacker["user_id"]}, {"$inc": {"balance": amount}})

    narration = await get_narrative("rob", get_mention(attacker), get_mention(target))

    await update.message.reply_text(
        f"💰 <b>ROBBERY!</b>\n\n📝 <i>{narration}</i>\n💸 <code>{format_money(amount)}</code>",
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

    users_collection.update_one({"user_id": sender["user_id"]}, {"$inc": {"balance": -cost}})
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

    users_collection.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": -REVIVE_COST}})
    users_collection.update_one({"user_id": user["user_id"]}, {"$set": {"status": "alive"}})

    await update.message.reply_text("💖 Revived!")
