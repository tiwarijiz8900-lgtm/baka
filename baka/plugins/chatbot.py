import os
import httpx
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from baka.database import chatbot_collection


# ======================================================
# 🔥 SETTINGS
# ======================================================

SAMBANOVA_API_KEY = os.getenv("SAMBANOVA_API_KEY")

AI_URL = "https://cloud.sambanova.ai/api/v1/chat/completions"
MODEL = "Meta-Llama-3-8B-Instruct"

MAX_HISTORY = 20   # memory

CHAT_ALWAYS_ON = True
TAG_ENABLED = False


# ======================================================
# 🔥 COMMANDS (ON/OFF + TAG)
# ======================================================

async def chaton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ALWAYS_ON
    CHAT_ALWAYS_ON = True
    await update.message.reply_text("✅ Chatbot ON baby 😘 Ab sirf tumse baat karungi")


async def chatoff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ALWAYS_ON
    CHAT_ALWAYS_ON = False
    await update.message.reply_text("❌ Chatbot OFF 😴")


async def tagon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global TAG_ENABLED
    TAG_ENABLED = True
    await update.message.reply_text("✅ Tag ON 🔥")


async def tagoff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global TAG_ENABLED
    TAG_ENABLED = False
    await update.message.reply_text("❌ Tag OFF")


async def tagall(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not TAG_ENABLED:
        return await update.message.reply_text("❌ Tag disabled")

    chat_id = update.effective_chat.id
    admins = await context.bot.get_chat_administrators(chat_id)

    mentions = []
    for m in admins:
        mentions.append(f"[{m.user.first_name}](tg://user?id={m.user.id})")

    await update.message.reply_text(
        " ".join(mentions),
        parse_mode="Markdown"
    )


# ======================================================
# 🔥 AI CALL (SAMBANOVA FAST)
# ======================================================

async def ask_ai_raw(messages):

    headers = {
        "Authorization": f"Bearer {SAMBANOVA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.95,
        "max_tokens": 120
    }

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(AI_URL, json=payload, headers=headers)

    if r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"].strip()

    return "Baby net slow hai 😭 phir bolo na"


# ======================================================
# 🔥 AI RESPONSE LOGIC
# ======================================================

async def get_ai_response(chat_id: int, text: str, name: str):

    doc = chatbot_collection.find_one({"chat_id": chat_id}) or {}
    history = doc.get("history", [])

    system_prompt = (
        f"You are a cute indian girlfriend chatbot. "
        f"User name is {name}. "
        f"Reply in short Hinglish. "
        f"Flirty, romantic, caring, sweet. "
        f"Max 1-2 lines only. "
        f"Use emojis. "
        f"Never long answers."
    )

    messages = [{"role": "system", "content": system_prompt}]

    for h in history[-MAX_HISTORY:]:
        messages.append(h)

    messages.append({"role": "user", "content": text})

    reply = await ask_ai_raw(messages)

    # save history
    history.append({"role": "user", "content": text})
    history.append({"role": "assistant", "content": reply})

    chatbot_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"history": history}},
        upsert=True
    )

    return reply


# ======================================================
# 🔥 MAIN AUTO REPLY (UNLIMITED)
# ======================================================

async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not CHAT_ALWAYS_ON:
        return

    msg = update.message
    if not msg or not msg.text:
        return

    if msg.text.startswith("/"):
        return

    name = msg.from_user.first_name

    await context.bot.send_chat_action(msg.chat.id, ChatAction.TYPING)

    reply = await get_ai_response(msg.chat.id, msg.text, name)

    # NORMAL TEXT (no stylize)
    await msg.reply_text(f"Hi {name} 😘 {reply}")


# ======================================================
# 🔥 /ask COMMAND
# ======================================================

async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        return await update.message.reply_text("Baby kuch pucho na 😚")

    text = " ".join(context.args)
    name = update.effective_user.first_name

    res = await get_ai_response(update.effective_chat.id, text, name)

    await update.message.reply_text(f"{res}")
