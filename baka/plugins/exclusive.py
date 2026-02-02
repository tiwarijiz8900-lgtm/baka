import random
from telegram import Update
from telegram.ext import ContextTypes
from baka.plugins.premium import is_premium
from baka.plugins.breakup import is_breakup
from baka.plugins.jealous import is_jealous

async def premium_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # 1. BREAKUP CHECK (Priority 1)
    if is_breakup(user_id):
        return await update.message.reply_text(
            "💔 **Breakup Mode ON hai!**\nAbhi aapka dil toota hua hai, romance mat kijiye. Pehle `/breakup off` karein. 🥺"
        )

    # 2. PREMIUM CHECK (Priority 2)
    if not await is_premium(user_id):
        return await update.message.reply_text(
            "❌ Arre re! Ye command sirf **Premium Members** ke liye hai. 💎\nAbhi `/premium` lein aur Angel ke saath maze karein! 😘"
        )

    # Message Reply Check
    if not update.message.reply_to_message:
        return await update.message.reply_text("✨ Jise pyaar jatana hai, uske message pe reply karo baby! ❤️")

    target_user = update.message.reply_to_message.from_user
    target_id = target_user.id
    target_name = target_user.first_name

    # 3. JEALOUS MODE CHECK (Priority 3)
    # Agar target user ka Jealous mode ON hai, toh action block hoga
    if is_jealous(target_id):
        return await update.message.reply_text(
            f"🚫 Oye! {target_name} ka **Jealous Mode** ON hai. \nInhe chhuna mana hai, varna inka partner gussa ho jayega! 😡🔥"
        )

    command = update.message.text.split()[0].replace("/", "").lower()

    # Actions Logic
    actions = {
        "hug": [
            f"🫂 {user.first_name} ne {target_name} ko zor se gale laga liya! Kitna sukoon hai na? ✨",
            f"🫂 Ek garam jhappi {target_name} ke liye! ❤️"
        ],
        "kiss": [
            f"💋 {user.first_name} ne {target_name} ke gaal pe ek pyaara sa kiss kiya! 😚",
            f"💋 Muaaaah! {user.first_name} ki taraf se {target_name} ke liye ek romantic kiss! 🔥"
        ],
        "flirt": [
            f"😏 {user.first_name}: '{target_name}, tumhari aankhein itni naseeli kyun hain?' ✨",
            f"🔥 {user.first_name}: '{target_name}, kya tum thak nahi jaati? Mere dimaag mein jo chalti rehti ho!' 😉"
        ]
    }

    if command in actions:
        reply = random.choice(actions[command])
        await update.message.reply_text(reply)
