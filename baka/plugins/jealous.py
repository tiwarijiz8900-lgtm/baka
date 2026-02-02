from telegram import Update
from telegram.ext import ContextTypes

# Dictionary to store status
JEALOUS_STATUS = {} 

async def jealous_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not context.args:
        status = "ON" if JEALOUS_STATUS.get(user_id, False) else "OFF"
        return await update.message.reply_text(f"🤨 Jealous Mode filhal **{status}** hai.\nUsage: `/jealous on` ya `/jealous off`")

    choice = context.args[0].lower()
    if choice == "on":
        JEALOUS_STATUS[user_id] = True
        await update.message.reply_text("🔥 **JEALOUS MODE: ON**\n\nAb agar aapka partner kisi aur se chipka, toh Angel ki khair nahi! 😤")
    elif choice == "off":
        JEALOUS_STATUS[user_id] = False
        await update.message.reply_text("😇 **JEALOUS MODE: OFF**\n\nTheek hai, ab aapka partner thoda 'social' ho sakta hai.")

def is_jealous(user_id):
    return JEALOUS_STATUS.get(user_id, False)
