from telegram import Update
from telegram.ext import ContextTypes

# Global Dictionary (Ise MongoDB mein bhi save kar sakte hain)
BREAKUP_STATUS = {} 

async def breakup_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in BREAKUP_STATUS:
        BREAKUP_STATUS[user_id] = False

    if not context.args:
        status = "ON" if BREAKUP_STATUS[user_id] else "OFF"
        return await update.message.reply_text(f"💔 Breakup Mode filhal **{status}** hai.\nUsage: `/breakup on` ya `/breakup off`")

    choice = context.args[0].lower()
    if choice == "on":
        BREAKUP_STATUS[user_id] = True
        await update.message.reply_text("💔 **BREAKUP MODE: ON**\n\nAb Angel aapko koi romantic commands use nahi karne degi. Ab sirf thukra ke mera pyaar... 🎶")
    elif choice == "off":
        BREAKUP_STATUS[user_id] = False
        await update.message.reply_text("❤️ **BREAKUP MODE: OFF**\n\nMubarak ho! Dil phir se jud gaya. Ab aap romantic ho sakte hain! ✨")

# Yeh function dusre plugins (exclusive.py) mein use hoga check karne ke liye
def is_breakup(user_id):
    return BREAKUP_STATUS.get(user_id, False)
