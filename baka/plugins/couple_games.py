import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

# ✅ SAME SambaNova AI function
from baka.plugins.chatbot import ask_ai_raw


# ======================================================
# 💑 AI GENERATOR
# ======================================================

async def generate(prompt: str):

    system = (
        "You are a fun Indian couple game generator. "
        "Generate very short Hinglish content. "
        "Romantic + funny + flirty. "
        "Max 1-2 lines only."
    )

    return await ask_ai_raw(system, prompt, 60)


# ======================================================
# 💗 TRUTH (UNLIMITED)
# ======================================================

async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):

    q = await generate("Give one funny truth question for couples.")

    if not q:
        q = "Secret crush ka naam batao 😏"

    await update.message.reply_text(
        f"💗 <b>TRUTH TIME</b>\n\n{q}",
        parse_mode=ParseMode.HTML
    )


# ======================================================
# 🔥 DARE (UNLIMITED)
# ======================================================

async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):

    d = await generate("Give one romantic or funny dare task.")

    if not d:
        d = "Group me kisi ko I love you bolo ❤️"

    await update.message.reply_text(
        f"🔥 <b>DARE TIME</b>\n\n{d}",
        parse_mode=ParseMode.HTML
    )


# ======================================================
# 🧠 QUIZ (UNLIMITED)
# ======================================================

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):

    q = await generate("Create one love quiz with answer included.")

    if not q:
        q = "Love ka opposite?\nA) Hate\nB) Care\nAnswer: A"

    await update.message.reply_text(
        f"🧠 <b>LOVE QUIZ</b>\n\n{q}",
        parse_mode=ParseMode.HTML
    )


# ======================================================
# 💑 RANDOM GAME (TRUTH/DARE/QUIZ auto mix)
# ======================================================

async def couplegame(update: Update, context: ContextTypes.DEFAULT_TYPE):

    choice = random.choice(["truth", "dare", "quiz"])

    if choice == "truth":
        await truth(update, context)
    elif choice == "dare":
        await dare(update, context)
    else:
        await quiz(update, context)
