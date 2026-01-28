import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

# ✅ use SAME samba function
from baka.plugins.chatbot import ask_ai_raw


async def generate(prompt):
    return await ask_ai_raw(
        "Generate short cute couple game content in Hinglish.",
        prompt,
        60
    )


# ---------------- TRUTH ----------------

async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = await generate("Give one funny truth question for couples.")

    if not q:
        q = "Secret crush ka naam batao 😏"

    await update.message.reply_text(f"💗 <b>TRUTH</b>\n\n{q}", parse_mode=ParseMode.HTML)


# ---------------- DARE ----------------

async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    d = await generate("Give one romantic or funny dare task.")

    if not d:
        d = "Group me kisi ko I love you bolo ❤️"

    await update.message.reply_text(f"🔥 <b>DARE</b>\n\n{d}", parse_mode=ParseMode.HTML)


# ---------------- QUIZ ----------------

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = await generate("Create one love quiz with answer.")

    if not q:
        q = "Love ka opposite?\nA) Hate\nB) Care\nAnswer: A"

    await update.message.reply_text(f"🧠 <b>QUIZ</b>\n\n{q}", parse_mode=ParseMode.HTML)
