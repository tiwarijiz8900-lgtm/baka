import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

# ✅ ECONOMY & UTILS IMPORTS
from baka.plugins.economy import get_balance, update_balance
from baka.utils import format_money, get_mention

# ✅ STATS LOGIC (Monthly Users Count karne ke liye)
# Ye functions aapke database plugin se aane chahiye
from baka.plugins.database import add_served_user, is_served_user

# =====================================
# ⚔️ 1v1 BATTLE (WITH STATS)
# =====================================

async def start_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.effective_message

    # 📈 STATS CHITTA: User ko DB mein count karna
    if not await is_served_user(user.id):
        await add_served_user(user.id)

    if not message.reply_to_message:
        return await message.reply_text(
            "⚔️ Kisi ke message pe reply karke challenge karo!"
        )

    enemy = message.reply_to_message.from_user
    
    # Opponent ko bhi DB mein count karna stats ke liye
    if not await is_served_user(enemy.id):
        await add_served_user(enemy.id)

    if user.id == enemy.id:
        return await message.reply_text("❌ Khud se ladoge kya? 😂")

    fee = 200

    # Balance Check
    user_bal = await get_balance(user.id)
    enemy_bal = await get_balance(enemy.id)

    if user_bal < fee:
        return await message.reply_text(
            f"💰 Tumhare paas {format_money(fee)} coins nahi hain!"
        )

    if enemy_bal < fee:
        return await message.reply_text(
            "⚠️ Opponent ke paas coins kam hain!"
        )

    msg = await message.reply_text(
        f"⚔️ {user.first_name} **VS** {enemy.first_name}\n\n"
        "Talwaren takra rahi hain... 🗡️",
        parse_mode=ParseMode.MARKDOWN
    )

    await asyncio.sleep(2)

    winner = random.choice([user, enemy])
    loser = enemy if winner.id == user.id else user

    # ✅ ECONOMY UPDATE (Coins Transfer)
    await update_balance(loser.id, -fee)
    await update_balance(winner.id, fee)

    await msg.edit_text(
        f"🏆 <b>BATTLE RESULT</b>\n\n"
        f"🥇 Winner: {get_mention(winner)}\n"
        f"💀 Loser: {get_mention(loser)}\n\n"
        f"💰 Won: <code>{format_money(fee)}</code>",
        parse_mode=ParseMode.HTML
    )


# =====================================
# 🔥 2v2 MULTI BATTLE (WITH STATS)
# =====================================

async def multi_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.effective_message
    
    # 📈 STATS CHITTA: User count for monthly stats
    if not await is_served_user(user.id):
        await add_served_user(user.id)

    if len(context.args) < 3:
        return await message.reply_text(
            "⚔️ Format:\n/multibattle @partner @enemy1 @enemy2"
        )

    fee = 300
    user_bal = await get_balance(user.id)

    if user_bal < fee:
        return await message.reply_text(
            f"💰 {format_money(fee)} coins chahiye!"
        )

    partner = context.args[0]
    enemy1 = context.args[1]
    enemy2 = context.args[2]

    msg = await message.reply_text(
        f"🔥 TEAM A: {user.first_name} & {partner}\n"
        f"VS\n"
        f"❄️ TEAM B: {enemy1} & {enemy2}\n\n"
        "Battle shuru... ⚡"
    )

    await asyncio.sleep(3)

    win_team = random.choice(["A", "B"])
    prize = fee * 2

    if win_team == "A":
        await update_balance(user.id, prize)
        result = (
            f"🏆 <b>TEAM A WON!</b>\n\n"
            f"{user.first_name} ne jeet liya!\n"
            f"💰 Prize: <code>{format_money(prize)}</code>"
        )
    else:
        await update_balance(user.id, -fee)
        result = (
            f"💀 <b>TEAM B WON!</b>\n\n"
            "Better luck next time!"
        )

    await msg.edit_text(result, parse_mode=ParseMode.HTML)
