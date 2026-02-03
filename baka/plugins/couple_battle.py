import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from motor.motor_asyncio import AsyncIOMotorClient # MongoDB ke liye

# ✅ ECONOMY & UTILS IMPORTS
from baka.plugins.economy import get_balance, update_balance
from baka.utils import format_money, get_mention
from baka.config import MONGO_DB_URI # Aapki config file se URI lega

# ✅ DIRECT DATABASE CONNECTION (Chitta)
db_client = AsyncIOMotorClient(MONGO_DB_URI)
db = db_client.Bot_8 # Database ka naam
users_db = db.users   # Collection ka naam

# Stats function isi file mein
async def track_user(user_id):
    user = await users_db.find_one({"user_id": user_id})
    if not user:
        await users_db.insert_one({"user_id": user_id})

# =====================================
# ⚔️ 1v1 BATTLE
# =====================================

async def start_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.effective_message

    # 📈 User Count Stats
    await track_user(user.id)

    if not message.reply_to_message:
        return await message.reply_text("⚔️ Reply karke challenge karo!")

    enemy = message.reply_to_message.from_user
    await track_user(enemy.id)

    if user.id == enemy.id:
        return await message.reply_text("❌ Khud se ladoge kya? 😂")

    fee = 200
    user_bal = await get_balance(user.id)
    enemy_bal = await get_balance(enemy.id)

    if user_bal < fee or enemy_bal < fee:
        return await message.reply_text("💰 Coins kam hain!")

    msg = await message.reply_text(f"⚔️ {user.first_name} VS {enemy.first_name}...")
    await asyncio.sleep(2)

    winner = random.choice([user, enemy])
    loser = enemy if winner.id == user.id else user

    await update_balance(loser.id, -fee)
    await update_balance(winner.id, fee)

    await msg.edit_text(
        f"🏆 Winner: {get_mention(winner)}\n💰 Won: {format_money(fee)}",
        parse_mode=ParseMode.HTML
    )

# =====================================
# 🔥 2v2 MULTI BATTLE
# =====================================

async def multi_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await track_user(user.id)

    if len(context.args) < 3:
        return await update.message.reply_text("⚔️ Format: /multibattle @p @e1 @e2")

    fee = 300
    if await get_balance(user.id) < fee:
        return await update.message.reply_text("💰 Coins nahi hain!")

    msg = await update.message.reply_text("🔥 Battle shuru... ⚡")
    await asyncio.sleep(3)

    if random.choice(["A", "B"]) == "A":
        await update_balance(user.id, fee * 2)
        res = "🏆 TEAM A WON!"
    else:
        await update_balance(user.id, -fee)
        res = "💀 TEAM B WON!"

    await msg.edit_text(res, parse_mode=ParseMode.HTML)
