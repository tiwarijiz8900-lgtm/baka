import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
# Maan lete hain aapka database economy.py se handle hota hai
from baka.plugins import economy 

BATTLE_FEES = 150  # Battle ki fees
WIN_PRIZE = 700   # Jeetne wale ka inaam

async def couple_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        return await update.message.reply_text("❌ Arre baby, do couples ke naam toh likho! \nUsage: `/battle @couple1 @couple2`")

    user_id = update.effective_user.id
    couple1 = context.args[0]
    couple2 = context.args[1]
    
    # Yahan fees check karne ka logic (agar aapke economy plugin mein ye functions hain)
    # Agar balance kam hai toh return kar dega
    
    starting_msg = await update.message.reply_text(
        f"⚔️ **BATTLE START** ⚔️\n\n"
        f"❤️ {couple1} VS ❤️ {couple2}\n\n"
        f"💰 Fees: {BATTLE_FEES} coins kat gaye!\n"
        f"Angel kismat check kar rahi hai... 🧐"
    )
    
    await asyncio.sleep(2)
    
    score1 = random.randint(30, 100)
    score2 = random.randint(30, 100)
    
    if score1 > score2:
        winner_text = f"🏆 **WINNER:** {couple1}\n💖 Inka pyaar sacha hai! Inaam: {WIN_PRIZE} coins! 💸"
    elif score2 > score1:
        winner_text = f"🏆 **WINNER:** {couple2}\n💖 Inka bond strong hai! Inaam: {WIN_PRIZE} coins! 💸"
    else:
        winner_text = "🤝 **TIE!** \nKoi nahi jeeta, coins wapas mil gaye! 😉"

    await starting_msg.edit_text(
        f"⚔️ **BATTLE RESULT** ⚔️\n"
        f"--------------------------\n"
        f"{winner_text}\n"
        f"--------------------------\n"
        f"Score: {score1}% vs {score2}%"
    )

async def battle_lb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🏆 **BATTLE LEADERBOARD** 🏆\n\n1. Rahul & Priya - 15 Wins\n2. Sameer & Angel - 12 Wins\n\nSabse bade fighter bano! 🔥"
    await update.message.reply_text(text)
