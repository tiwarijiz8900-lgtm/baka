import random
from telegram import Update
from telegram.ext import ContextTypes
from baka.plugins.economy import get_balance, update_balance

async def multi_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Example command: /multibattle @partner1 @enemy1 @enemy2
    if len(context.args) < 3:
        return await update.message.reply_text("❌ **Usage:** `/multibattle @partner @enemy1 @enemy2`\n\nIsme 2 couples ki jung hogi! ⚔️")

    user = update.effective_user
    partner = context.args[0]
    enemy1 = context.args[1]
    enemy2 = context.args[2]

    # Entry Fee
    fee = 250
    if await get_balance(user.id) < fee:
        return await update.message.reply_text(f"💰 Battle ke liye kam se kam {fee} coins chahiye!")

    # Battle Animation/Text
    await update.message.reply_text(f"⚔️ **MEGA BATTLE START!** ⚔️\n\n❤️ **TEAM A:** {user.first_name} & {partner}\n      **VS**\n💙 **TEAM B:** {enemy1} & {enemy2}\n\nJung jaari hai... 🛡️")

    # Result Calculation
    win_chance = random.choice(["A", "B"])
    prize = fee * 2

    if win_chance == "A":
        await update_balance(user.id, prize)
        result = f"🏆 **TEAM A JEET GAYI!** 🏆\n\n{user.first_name} aur {partner} ne milkar {enemy1} aur {enemy2} ki dhajjiyan uda di! \n💰 Prize: {prize} coins Team A ko mile!"
    else:
        result = f"💀 **TEAM B JEET GAYI!** 💀\n\n{enemy1} aur {enemy2} ne Team A ko dhool chata di! \n🔥 {user.first_name}, agli baar taiyari karke aana!"

    await update.message.reply_text(result)
