from telegram import Update
from telegram.ext import ContextTypes

async def link_guard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    # Admins ko allow karte hain
    member = await chat.get_member(user.id)
    if member.status in ['creator', 'administrator']:
        return

    # Agar text mein URL hai
    if message.entities:
        for entity in message.entities:
            if entity.type in ['url', 'text_link']:
                try:
                    await message.delete()
                    warn_msg = await context.bot.send_message(
                        chat_id=chat.id,
                        text=f"🚫 **ANTI-LINK GUARD** 🚫\n\nHey {user.first_name}, links bhejna yahan mana hai! Dubara mat karna. 🤫"
                    )
                    # 5 second baad warning message delete kar dete hain
                    await asyncio.sleep(5)
                    await warn_msg.delete()
                except Exception as e:
                    print(f"Error deleting link: {e}")
                break
