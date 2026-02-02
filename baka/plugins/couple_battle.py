import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes

async def couple_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Command format: /battle @user1 @user2
    if len(context.args) < 2:
        return await update.message.reply_text("❌ Arre baby, do couples ke naam toh likho! \nUsage: `/battle @couple1 @couple2`", parse_mode="Markdown")

    couple1 = context.args[0]
    couple2 = context.args[1]
    
    name = update.effective_user.first_name
    
    # Battle animation messages
    starting_msg = await update.message.reply_text(f"⚔️ **BATTLE START** ⚔️\n\n❤️ {couple1} \n      VS \n❤️ {couple2}\n\nAngel kismat check kar rahi hai... 🧐")
    
    await asyncio.sleep(2) # 2 second wait for drama
    
    # Random Score calculation (0 to 100)
    score1 = random.randint(40, 100)
    score2 = random.randint(40, 100)
    
    if score1 > score2:
        winner = couple1
        result_text = f"🏆 **WINNER:** {couple1} \n\n💖 Inka pyaar zyada gehra hai! ({score1}% vs {score2}%)"
    elif score2 > score1:
        winner = couple2
        result_text = f"🏆 **WINNER:** {couple2} \n\n💖 Inka bond unbeatable hai! ({score2}% vs {score1}%)"
    else:
        result_text = f"🤝 **TIE!** \n\nDono couples ek se badhkar ek hain! ({score1}%)"

    final_msg = (
        f"⚔️ **BATTLE OVER** ⚔️\n"
        f"--------------------------\n"
        f"{result_text}\n"
        f"--------------------------\n"
        f"Angel ki dua dono ke saath hai! 😘"
    )
    
    await starting_msg.edit_text(final_msg)

# Leaderboard preview logic
async def battle_lb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🏆 **COUPLE BATTLE LEADERBOARD** 🏆\n"
        "1. Rahul & Priya - 15 Wins\n"
        "2. Sameer & Angel - 12 Wins\n"
        "3. Rohit & Sneha - 08 Wins\n\n"
        "Battle jeeto aur top pe aao! 🔥"
    )
    await update.message.reply_text(text)
