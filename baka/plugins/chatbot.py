import os
import httpx
import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction, ChatType

from baka.database import chatbot_collection
from baka.utils import stylize_text

# ======================================================
# 🔥 SETTINGS
# ======================================================

SAMBANOVA_API_KEY = os.getenv("SAMBANOVA_API_KEY")

AI_URL = "https://api.sambanova.ai/v1/chat/completions"
MODEL = "Meta-Llama-3-8B-Instruct"

MAX_HISTORY = 15

CHAT_ALWAYS_ON = True
TAG_ENABLED = False


# ======================================================
# 🔥 COMMANDS (ON/OFF + TAG)
# ======================================================

async def chaton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ALWAYS_ON
    CHAT_ALWAYS_ON = True
    await update.message.reply_text("✅ Chatbot ON baby 😘")


async def chatoff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ALWAYS_ON
    CHAT_ALWAYS_ON = False
    await update.message.reply_text("❌ Chatbot OFF")


async def tagon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global TAG_ENABLED
    TAG_ENABLED = True
    await update.message.reply_text("✅ Tag ON")


async def tagoff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global TAG_ENABLED
    TAG_ENABLED = False
    await update.message.reply_text("❌ Tag OFF")


async def tagall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not TAG_ENABLED:
        return await update.message.reply_text("Tag disabled")

    members = []
    admins = await context.bot.get_chat_administrators(update.effective_chat.id)

    for m in admins:
        members.append(f"[{m.user.first_name}](tg://user?id={m.user.id})")

    await update.message.reply_text(" ".join(members), parse_mode="Markdown")


# ======================================================
# 🔥 AI FUNCTION (SAMBANOVA)
# ======================================================

async def ask_ai_raw(messages):

    headers = {
        "Authorization": f"Bearer {SAMBANOVA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.9,
        "max_tokens": 120
    }

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(AI_URL, json=payload, headers=headers)

    if r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"]

    return "Net slow hai baby 😭"


# ======================================================
# 🔥 AI RESPONSE
# ======================================================

async def get_ai_response(chat_id: int, text: str, name: str):

    doc = chatbot_collection.find_one({"chat_id": chat_id}) or {}
    history = doc.get("history", [])

    system_prompt = (
        f"Tum ek cute Indian girlfriend ho. "
        f"User ka naam {name} hai. "
        f"Short Hinglish reply do. Flirty + sweet + caring. "
        f"Max 1-2 line. Emoji use karo."
    )

    messages = [{"role": "system", "content": system_prompt}]

    for h in history[-MAX_HISTORY:]:
        messages.append(h)

    messages.append({"role": "user", "content": text})

    reply = await ask_ai_raw(messages)

    history.append({"role": "user", "content": text})
    history.append({"role": "assistant", "content": reply})

    chatbot_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"history": history}},
        upsert=True
    )

    return reply


# ======================================================
# 🔥 MAIN MESSAGE HANDLER (UNLIMITED AUTO REPLY)
# ======================================================

async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not CHAT_ALWAYS_ON:
        return

    msg = update.message
    if not msg or not msg.text:
        return

    if msg.text.startswith("/"):
        return

    chat = update.effective_chat
    name = msg.from_user.first_name

    await context.bot.send_chat_action(chat.id, ChatAction.TYPING)

    reply = await get_ai_response(chat.id, msg.text, name)

    await msg.reply_text(f"Hi {name} 😘 {stylize_text(reply)}")


# ======================================================
# 🔥 /ask command
# ======================================================

async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        return await update.message.reply_text("/ask kuch likho baby")

    text = " ".join(context.args)
    name = update.effective_user.first_name

    res = await get_ai_response(update.effective_chat.id, text, name)

    await update.message.reply_text(res)
