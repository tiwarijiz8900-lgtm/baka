import random
from telegram import Update
from telegram.ext import ContextTypes

# ✅ FIXED IMPORTS
from baka.plugins.premium import check_premium as is_premium
from baka.plugins.breakup import is_breakup
from baka.plugins.jealous import is_jealous


# =========================================
# 💎 PREMIUM ACTION COMMANDS (hug/kiss/flirt)
# =========================================

async def premium_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    # ==============================
    # 1️⃣ BREAKUP CHECK
    # ==============================
    if is_breakup(user_id):
        return await update.message.reply_text(
            "💔 Breakup Mode ON hai!\nPehle `/breakup off` karo baby 🥺"
        )

    # ==============================
    # 2️⃣ PREMIUM CHECK (FIXED)
    # ==============================
    # ❌ await removed (normal function hai)
    if not is_premium(user_id):
        return await update.message.reply_text(
            "❌ Ye command sirf Premium Members ke liye hai 💎\n/premium lelo jaan 😘"
        )

    # ==============================
    # Reply check
    # ==============================
    if not update.message.reply_to_message:
        return await update.message.reply_text(
            "✨ Jise pyaar jatana hai uske message pe reply karo ❤️"
        )

    target_user = update.message.reply_to_message.from_user
    target_id = target_user.id
    target_name = target_user.first_name

    # ==============================
    # 3️⃣ JEALOUS CHECK
    # ==============================
    if is_jealous(target_id):
        return await update.message.reply_text(
            f"🚫 {target_name} ka Jealous Mode ON hai!\nDoor raho warna partner gussa ho jayega 😡🔥"
        )

    # ==============================
    # COMMAND NAME
    # ==============================
    command = update.message.text.split()[0].replace("/", "").lower()

    # ==============================
    # ACTIONS
    # ==============================
    actions = {
        "hug": [
            f"🫂 {user.first_name} ne {target_name} ko zor se gale laga liya ❤️",
            f"🫂 Ek tight hug {target_name} ke liye ✨"
        ],
        "kiss": [
            f"💋 {user.first_name} ne {target_name} ko pyaara sa kiss diya 😘",
            f"💋 Muaaaah! {target_name} blush ho gaya 🔥"
        ],
        "flirt": [
            f"😏 {target_name}, tumhari smile bohot dangerous hai ❤️",
            f"🔥 {user.first_name}: Tum mere dil pe attack kar rahi ho kya? 😉"
        ]
    }

    # ==============================
    # SEND REPLY
    # ==============================
    if command in actions:
        reply = random.choice(actions[command])
        await update.message.reply_text(reply)
