import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from baka.plugins.economy import get_balance, update_balance

# Gangs storage logic (In-memory for now, use DB for permanent)
GANGS = {} 

async def attack_gang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if len(context.args) < 1:
        return await update.message.reply_text("⚔️ **Usage:** `/attack [GangName]`\nKiske vault pe hamla karna hai?")

    target_gang = " ".join(context.args)
    
    if target_gang not in GANGS:
        return await update.message.reply_text("❌ Ye gang exist nahi karti!")

    # Attack Animation
    msg = await update.message.reply_text(f"🧨 **ATTACK!** {user.first_name} ki gang ne {target_gang} ke vault pe bomb laga diya hai...")
    await asyncio.sleep(2)

    # Success Logic (50-50 Chance)
    success = random.choice([True, False])
    
    if success:
        stolen_coins = random.randint(2000, 8000)
        GANGS[target_gang]["vault"] -= stolen_coins
        await update_balance(user.id, stolen_coins)
        await msg.edit_text(f"🔥 **HEIST SUCCESS!** 🔥\n\nAapne {target_gang} ke vault se {stolen_coins} coins chura liye! 💰💨")
    else:
        penalty = 1500
        await update_balance(user.id, -penalty)
        await msg.edit_text(f"💀 **FAILED!** {target_gang} ke guards ne aapko peet kar bhaga diya. \n💸 Penalty: {penalty} coins.")

async def gang_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("🔎 Gang ka naam likho: `/ganginfo [Name]`")
    
    name = " ".join(context.args)
    if name in GANGS:
        g = GANGS[name]
        await update.message.reply_text(f"🛡️ **GANG:** {name}\n👑 **Leader:** {g['leader']}\n💰 **Vault:** {g['vault']} coins")
    else:
        await update.message.reply_text("❌ Gang nahi mili.")
