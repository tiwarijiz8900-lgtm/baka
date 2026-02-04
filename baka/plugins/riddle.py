from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatType

# ✅ FIXED → GROQ import
try:
    from baka.plugins.chatbot import ask_groq
except:
    ask_groq = None

from baka.database import riddles_collection, users_collection
from baka.utils import format_money, ensure_user_exists, get_mention
from baka.config import RIDDLE_REWARD


# =====================================================
# 🧩 START RIDDLE
# =====================================================

async def riddle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        return await update.message.reply_text("❌ Group Only!")

    if riddles_collection.find_one({"chat_id": chat.id}):
        return await update.message.reply_text("⚠️ A riddle is already active!")

    msg = await update.message.reply_text("🧠 Generating AI Riddle...")

    prompt = (
        "Generate a short hard riddle.\n"
        "Format EXACTLY:\n"
        "Riddle: question | Answer: oneword"
    )

    response = None

    # ✅ GROQ safe call
    if ask_groq:
        try:
            response = await ask_groq(prompt)
        except:
            response = None

    if not response or "|" not in str(response):
        return await msg.edit_text("⚠️ AI failed. Try again.")

    try:
        parts = response.split("|")
        question = parts[0].replace("Riddle:", "").strip()
        answer = parts[1].replace("Answer:", "").strip().lower()
    except:
        return await msg.edit_text("⚠️ AI parse error.")

    riddles_collection.insert_one({
        "chat_id": chat.id,
        "answer": answer
    })

    await msg.edit_text(
        f"🧩 <b>AI Riddle Challenge!</b>\n\n"
        f"<i>{question}</i>\n\n"
        f"💰 Reward: <code>{format_money(RIDDLE_REWARD)}</code>\n"
        f"Reply with answer!",
        parse_mode=ParseMode.HTML
    )


# =====================================================
# ✅ CHECK ANSWER
# =====================================================

async def check_riddle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    chat = update.effective_chat
    text = update.message.text.strip().lower()

    riddle = riddles_collection.find_one({"chat_id": chat.id})
    if not riddle:
        return

    if text == riddle['answer']:
        user = update.effective_user
        ensure_user_exists(user)

        users_collection.update_one(
            {"user_id": user.id},
            {"$inc": {"balance": RIDDLE_REWARD}}
        )

        riddles_collection.delete_one({"chat_id": chat.id})

        await update.message.reply_text(
            f"🎉 <b>Correct!</b>\n\n"
            f"👤 {get_mention(user)}\n"
            f"💰 Won: <code>{format_money(RIDDLE_REWARD)}</code>\n"
            f"🔑 Answer: <i>{riddle['answer'].title()}</i>",
            parse_mode=ParseMode.HTML
    )
