from telegram import Update
from telegram.ext import ContextTypes

# Dictionary to store status
FLIRT_STATUS = {} 

async def flirt_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not context.args:
        status = "ON" if FLIRT_STATUS.get(user_id, False) else "OFF"
        return await update.message.reply_text(f"😘 Flirt Mode filhal **{status}** hai.\nUsage: `/flirtmode on` ya `/flirtmode off`")

    choice = context.args[0].lower()
    if choice == "on":
        FLIRT_STATUS[user_id] = True
        await update.message.reply_text("🔥 **FLIRT MODE: ON**\n\nAb Angel thodi zayda hi romantic ho jayegi. Sambhal lena! 😉✨")
    elif choice == "off":
        FLIRT_STATUS[user_id] = False
        await update.message.reply_text("😇 **FLIRT MODE: OFF**\n\nTheek hai, ab hum sirf ache dost hain.")

def is_flirt_on(user_id):
    return FLIRT_STATUS.get(user_id, False)
