import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

# ✅ SAHI IMPORTS (Economy se functions uthaye hain)
from baka.plugins.economy import get_balance, update_balance
from baka.utils import format_money, get_mention
from baka.database import users_collection # Motor hata kar standard collection use kiya hai

# ===============================
# USER TRACKER (Fixed for PyMongo)
# ===============================
async def track_user(user_id):
    """Battle stats update karne ke liye"""
    user = users_collection.find_one({"user_id": user_id})
    if not user:
        users_collection.insert_one({
            "user_id": user_id,
            "battles": 0,
            "balance": 0
        })

# =====================================
# ⚔️ 1v1 BATTLE
# =====================================
async def start_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.effective_message

    await track_user(user.id)

    if not message.reply_to_message:
        return await message.reply_text("⚔️ Kisi dushman ke message pe reply karke challenge karo!")

    enemy = message.reply_to_message.from_user
    await track_user(enemy.id)

    if user.id == enemy.id:
        return await message.reply_text("❌ Khud se ladoge toh hospital kaun le jayega? 😂")

    fee = 200

    # ✅ Economy fix
    user_bal = await get_balance(user.id)
    enemy_bal = await get_balance(enemy.id)

    if user_bal < fee:
        return await message.reply_text(f"💰 Aapke paas {format_money(fee)} nahi hain!")
    
    if enemy_bal < fee:
        return await message.reply_text(f"💰 Saamne wale ke paas {format_money(fee)} nahi hain!")

    msg = await message.reply_text(f"⚔️ {user.first_name} VS {enemy.first_name}\n\n<i>Talwaren nikal rahi hain... 🗡️</i>", parse_mode=ParseMode.HTML)
    await asyncio.sleep(2)

    winner = random.choice([user, enemy])
    loser = enemy if winner.id == user.id else user

    # ✅ Balance Updates
    await update_balance(loser.id, -fee)
    await update_balance(winner.id, fee)
    
    # Track battle count
    users_collection.update_many({"user_id": {"$in": [user.id, enemy.id]}}, {"$inc": {"battles": 1}})

    await msg.edit_text(
        f"🏆 <b>BATTLE RESULT</b> 🏆\n\n"
        f"🥇 <b>Winner:</b> {get_mention(winner)}\n"
        f"💀 <b>Loser:</b> {get_mention(loser)}\n\n"
        f"💰 Winner ne {format_money(fee)} coins loot liye!",
        parse_mode=ParseMode.HTML
    )

# =====================================
# 🔥 2v2 MULTI BATTLE
# =====================================
async def multi_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    fee = 300

    if await get_balance(user.id) < fee:
        return await update.message.reply_text(f"💰 Is mega battle ke liye {format_money(fee)} chahiye!")

    msg = await update.message.reply_text("🔥 <b>Mega Battle Shuru Ho Rahi Hai...</b> ⚡", parse_mode=ParseMode.HTML)
    await asyncio.sleep(3)

    if random.choice(["A", "B"]) == "A":
        await update_balance(user.id, fee * 2)
        res = f"🏆 <b>TEAM A JEET GAYI!</b>\n\n{user.first_name} ko {format_money(fee*2)} ka inaam mila!"
    else:
        await update_balance(user.id, -fee)
        res = f"💀 <b>TEAM B JEET GAYI!</b>\n\n{user.first_name} ne {format_money(fee)} gawa diye!"

    await msg.edit_text(res, parse_mode=ParseMode.HTML)
