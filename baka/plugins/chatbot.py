import os
import httpx
import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

# ======================================================
# 🔥 SIMBAVY SETTINGS (FAST & UNLIMITED)
# ======================================================

SIMBAVY_API_URL = "https://api.simbavy.xyz/api/chat?message="
CHAT_ALWAYS_ON = True

# Angel replies (randomly pick karega jab koi 'angel' bolega)
ANGEL_REPLIES = [
    "Ji meri jaan, bolo? 😘",
    "Angel hamesha tumhare saath hai baby.. ❤️",
    "Hukum kijiye mere hero, angel haazir hai 😇",
    "I love it when you call me Angel! 😍"
]

# ======================================================
# 🔥 COMMANDS
# ======================================================

async def chaton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ALWAYS_ON
    CHAT_ALWAYS_ON = True
    await update.message.reply_text("✅ Chatbot ON! Ab har message ka reply milega 😘")

async def chatoff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ALWAYS_ON
    CHAT_ALWAYS_ON = False
    await update.message.reply_text("❌ Chatbot OFF! 😴")

# ======================================================
# 🔥 SIMBAVY API LOGIC
# ======================================================

async def get_simbavy_response(text: str):
    try:
        # API call with timeout
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{SIMBAVY_API_URL}{text}")
            if response.status_code == 200:
                data = response.json()
                # 'result' field se text nikalna
                reply = data.get("result", "Mujhe samajh nahi aaya baby.")
                return reply
            return "Net slow hai baby 😭"
    except Exception:
        return "Server busy hai, thoda ruko 😴"

# ======================================================
# 🔥 MAIN AUTO REPLY (EVERY MESSAGE)
# ======================================================

async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not CHAT_ALWAYS_ON:
        return

    msg = update.message
    if not msg or not msg.text or msg.text.startswith("/"):
        return

    incoming_text = msg.text.lower()
    name = msg.from_user.first_name

    # Typing action dikhane ke liye
    await context.bot.send_chat_action(msg.chat.id, ChatAction.TYPING)

    # API response lena
    api_reply = await get_simbavy_response(msg.text)

    # Angel Logic + Normal Response
    if "angel" in incoming_text:
        special_msg = random.choice(ANGEL_REPLIES)
        # Seedha saadha text, no style
        final_text = f"{special_msg}\n\n{api_reply}"
    else:
        # Normal chota message
        final_text = api_reply

    # Har message pe fast unlimited reply
    await msg.reply_text(final_text)

# ======================================================
# 🔥 /ask COMMAND
# ======================================================

async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Baby kuch toh pucho 😚")

    text = " ".join(context.args)
    res = await get_simbavy_response(text)
    await update.message.reply_text(res)
