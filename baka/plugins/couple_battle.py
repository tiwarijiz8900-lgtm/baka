import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from baka.plugins.economy import get_balance, update_balance

# --- Battle Logic ---
async def couple_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """1v1 Simple Battle"""
    user = update.effective_user
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚔️ Kisi dushman ke message pe reply karke use challenge karo!")

    enemy = update.message.reply_to_message.from_user
    if user.id == enemy.id:
        return await update.message.reply_text("❌ Khud se hi ladoge kya? Pagal ho gaye ho! 😂")

    # Coins Check
    fee = 200
    user_bal = await get_balance(user.id)
    if user_bal < fee:
        return await update.message.reply_text(f"💰 Battle ke liye {fee} coins chahiye, tumhare paas sirf {user_bal} hain!")

    # Animation
    msg = await update.message.reply_text(f"⚔️ {user.first_name} VS {enemy.first_name}\n\nTalwaren nikal rahi hain... 🗡️")
    await asyncio.sleep(2)

    # Result
    winner = random.choice([user, enemy])
    loser = enemy if winner.id == user.id else user
    
    prize = fee * 2
    await update_balance(winner.id, prize)
    await update_balance(loser.id, -fee)

    await msg.edit_text(
        f"🏆 **BATTLE RESULT** 🏆\n\n"
        f"🥇 Winner: {winner.first_name}\n"
        f"💀 Loser: {loser.first_name}\n\n"
        f"💰 {winner.first_name} ne {prize} coins jeet liye!"
    )

async def multi_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """2v2 Multi-Couple Battle"""
    user = update.effective_user
    if len(context.args) < 3:
        return await update.message.reply_text(
            "⚔️ **2v2 Battle Format:**\n"
            "`/multibattle @partner @enemy1 @enemy2`"
        )

    # Entry Fee
    fee = 300 
    user_bal = await get_balance(user.id)
    if user_bal < fee:
        return await update.message.reply_text(f"💰 Mega Battle ke liye {fee} coins chahiye!")

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

    # Result
    win_team = random.choice(["A", "B"])
    prize = fee * 2

    if win_team == "A":
        await update_balance(user.id, prize)
        result = f"🏆 **TEAM A JEET GAYI!** 🏆\n\n{user.first_name} aur {partner} ne maidan maar liya! 💰 Prize: {prize} coins!"
    else:
        result = f"💀 **TEAM B JEET GAYI!** 💀\n\n{enemy1} aur {enemy2} ne Team A ko dhool chata di! 🔥"

    await msg.edit_text(result)

async def battle_lb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Battle Leaderboard (Top Warriors)"""
    # Isme aap top winners ki list show kar sakte hain MongoDB se fetch karke
    await update.message.reply_text("🥇 **TOP WARRIORS** 🥇\n\nAbhi ranks calculate ho rahi hain... 📊")
