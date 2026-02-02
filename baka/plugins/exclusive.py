import random
from telegram import Update
from telegram.ext import ContextTypes
from baka.plugins.premium import is_premium

async def premium_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # Premium Check
    if not await is_premium(user_id):
        return await update.message.reply_text("❌ Arre re! Ye command sirf **Premium Members** ke liye hai. 💎\nAbhi `/premium` lein aur Angel ke saath maze karein! 😘")

    if not update.message.reply_to_message:
        return await update.message.reply_text("✨ Jise pyaar jatana hai, uske message pe reply karo baby! ❤️")

    target = update.message.reply_to_message.from_user.first_name
    command = update.message.text.split()[0].replace("/", "").lower()

    # Actions Logic
    actions = {
        "hug": [f"🫂 {user.first_name} ne {target} ko zor se gale laga liya! Kitna sukoon hai na? ✨", "🫂 Ek garam jhappi {target} ke liye! ❤️"],
        "kiss": [f"💋 {user.first_name} ne {target} ke gaal pe ek pyaara sa kiss kiya! 😚", "💋 Muaaaah! {user.first_name} ki taraf se {target} ke liye ek romantic kiss! 🔥"],
        "flirt": [f"😏 {user.first_name}: '{target}, tumhari aankhein itni naseeli kyun hain?' ✨", f"🔥 {user.first_name}: '{target}, kya tum thak nahi jaati? Din bhar mere dimaag mein jo chalti rehti ho!' 😉"]
    }

    if command in actions:
        reply = random.choice(actions[command])
        await update.message.reply_text(reply)
