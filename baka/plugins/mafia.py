import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from baka.plugins.economy import get_balance, update_balance

# Gangs storage
GANGS = {} # {gang_name: {"leader": id, "members": [ids], "vault": 0}}

async def create_gang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not context.args:
        return await update.message.reply_text("🕵️ Gang ka naam toh batao! Usage: `/creategang [name]`")
    
    gang_name = " ".join(context.args)
    if gang_name in GANGS:
        return await update.message.reply_text("❌ Ye Gang pehle se bani hui hai!")

    GANGS[gang_name] = {"leader": user.id, "members": [user.id], "vault": 0}
    await update.message.reply_text(f"🔥 **MAFIA GANG CREATED!** 🔥\n\nAb aap **{gang_name}** ke Don hain! `/joingang {gang_name}` se logo ko bulaiye.")

async def rob_bank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    # 30% Chance of getting caught
    success = random.choices([True, False], weights=[70, 30])[0]
    
    if success:
        loot = random.randint(5000, 15000)
        await update_balance(user_id, loot)
        await update.message.reply_text(f"💰 **HEIST SUCCESSFUL!** 💰\n\n{user.first_name} ne bank loot liya aur {loot} coins le kar faraar ho gaya! 🚓💨")
    else:
        fine = 2000
        await update_balance(user_id, -fine)
        await update.message.reply_text(f"👮 **BUSTED!** 👮\n\nPolice ne {user.first_name} ko pakad liya! Jail ho gayi aur {fine} coins ka jurmana laga. 🚔")
