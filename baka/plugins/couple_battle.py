import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from baka.database import users_collection
from baka.utils import format_money, get_mention

# --- Helper Functions (Fixes ImportErrors) ---
async def get_user_bal(user_id: int):
    """Directly fetch balance from DB to avoid import loops."""
    user = users_collection.find_one({"user_id": user_id})
    return user.get("balance", 0) if user else 0

async def update_user_bal(user_id: int, amount: int):
    """Directly update balance in DB."""
    users_collection.update_one({"user_id": user_id}, {"$inc": {"balance": amount}})

# --- Battle Logic ---
async def start_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """1v1 Simple Battle (Fixes the function name from your Ryan.py)"""
    user = update.effective_user
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚔️ Kisi dushman ke message pe reply karke use challenge karo!")

    enemy = update.message.reply_to_message.from_user
    if user.id == enemy.id:
        return await update.message.reply_text("❌ Khud se hi ladoge kya? Pagal ho gaye ho! 😂")

    # Entry Fee
    fee = 200
    user_bal = await get_user_bal(user.id)
    enemy_bal = await get_user_bal(enemy.id)

    if user_bal < fee:
        return await update.message.reply_text(f"💰 Battle ke liye {format_money(fee)} coins chahiye, tumhare paas sirf {format_money(user_bal)} hain!")
    
    if enemy_bal < fee:
        return await update.message.reply_text(f"⚠️ Samne wale ke paas {format_money(fee)} coins nahi hain ladne ke liye!")

    # Animation
    msg = await update.message.reply_text(f"⚔️ {user.first_name} **VS** {enemy.first_name}\n\nTalwaren nikal rahi hain... 🗡️", parse_mode=ParseMode.MARKDOWN)
    await asyncio.sleep(2)

    # Result Calculation
    winner = random.choice([user, enemy])
    loser = enemy if winner.id == user.id else user
    
    prize = fee # Winner gets the fee from loser
    await update_user_bal(winner.id, prize)
    await update_user_bal(loser.id, -fee)

    await msg.edit_text(
        f"🏆 **BATTLE RESULT** 🏆\n\n"
        f"🥇 **Winner:** {get_mention(winner)}\n"
        f"💀 **Loser:** {get_mention(loser)}\n\n"
        f"💰 {winner.first_name} ne {format_money(prize)} coins loot liye!",
        parse_mode=ParseMode.HTML
    )

async def multi_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """2v2 Multi-Couple Battle"""
    user = update.effective_user
    if len(context.args) < 3:
        return await update.message.reply_text(
            "⚔️ **2v2 Battle Format:**\n"
            "`/multibattle @partner @enemy1 @enemy2`",
            parse_mode=ParseMode.MARKDOWN
        )

    fee = 300 
    user_bal = await get_user_bal(user.id)
    if user_bal < fee:
        return await update.message.reply_text(f"💰 Mega Battle ke liye {format_money(fee)} coins chahiye!")

    partner = context.args[0]
    enemy1 = context.args[1]
    enemy2 = context.args[2]

    msg = await update.message.reply_text(
        f"🔥 **TEAM A:** {user.first_name} & {partner}\n"
        f"       **VS**\n"
        f"❄️ **TEAM B:** {enemy1} & {enemy2}\n\n"
        "Badi jung shuru ho gayi hai! 🛡️⚡"
    )
    await asyncio.sleep(3)

    win_team = random.choice(["A", "B"])
    prize = fee * 2

    if win_team == "A":
        await update_user_bal(user.id, prize)
        result = f"🏆 **TEAM A JEET GAYI!** 🏆\n\n{user.first_name} aur {partner} ne maidan maar liya! 💰 Prize: {format_money(prize)} coins!"
    else:
        result = f"💀 **TEAM B JEET GAYI!** 💀\n\n{enemy1} aur {enemy2} ne Team A ko dhool chata di! 🔥"

    await msg.edit_text(result)
