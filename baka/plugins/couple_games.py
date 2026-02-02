import httpx
import random
from telegram import Update
from telegram.ext import ContextTypes

# Free API Endpoints
TRUTH_API = "https://api.truthordarebot.xyz/v1/truth"
DARE_API = "https://api.truthordarebot.xyz/v1/dare"

# ======================================================
# 🔥 UNLIMITED TRUTH (From API)
# ======================================================

async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(TRUTH_API)
            if response.status_code == 200:
                question = response.json().get("question")
                # Angel theme reply
                await update.message.reply_text(f"✨ **TRUTH FOR {name}** ✨\n\nQuestion: {question}\n\nJhoot mat bolna, Angel sab dekh rahi hai! 😉")
            else:
                await update.message.reply_text("API busy hai baby, thoda ruko! 😴")
    except Exception:
        await update.message.reply_text("Net slow hai, fir se try karo 🥺")

# ======================================================
# 🔥 UNLIMITED DARE (From API)
# ======================================================

async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(DARE_API)
            if response.status_code == 200:
                task = response.json().get("question")
                await update.message.reply_text(f"🔥 **DARE FOR {name}** 🔥\n\nTask: {task}\n\nPure nahi kiya toh Angel naraz ho jayegi! 😘")
            else:
                await update.message.reply_text("API down hai baby 😴")
    except Exception:
        await update.message.reply_text("Kuch galat hua, phir se try karo! ❌")

# ======================================================
# 🧠 UNLIMITED QUIZ (Mix Logic)
# ======================================================

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Quiz ke liye hum ek badi list rakhenge kyunki ye special love-related hai
    QUIZZES = [
        "Agar hum kisi island pe phas gaye, toh tum kya karoge? 🤔",
        "Tumhare hisab se sacha pyaar kya hai? ❤️",
        "Relationship mein sabse badi galti kya ho sakti hai? 💔",
        "Kya tum mujhse kabhi bore hoge? 🥺",
        "Pehli nazar ka pyaar sach hota hai? ✨"
    ]
    await update.message.reply_text(f"🧠 **LOVE QUIZ** 🧠\n\nSawal: {random.choice(QUIZZES)}\n\nAngel tumhara jawab sunna chahti hai! ❤️")
