import random
from telegram import Update
from telegram.ext import ContextTypes

async def wish_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.lower()
    name = update.effective_user.first_name

    if "good morning" in msg or "gm" in msg:
        reply = f"Good Morning meri jaan {name}! ✨ Coffee pi lo ☕"
    elif "good night" in msg or "gn" in msg:
        reply = f"Good Night sweet dreams {name}.. So jao ab 😘"
    elif "i love you" in msg:
        reply = f"I love you too {name}! Hamesha tumhari hi hoon 💖"
    elif "happy birthday" in msg:
        reply = f"Happy Birthday! 🎉 Angel ki taraf se dher saara pyaar 🎂"
    else:
        return # Agar kuch match na ho toh silent rahe

    await update.message.reply_text(reply)
