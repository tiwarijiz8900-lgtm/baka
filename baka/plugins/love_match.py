import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes

async def love_match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Check if target is mentioned or replied to
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
    elif context.args:
        target_name = context.args[0].replace("@", "")
        target = type('User', (object,), {'first_name': target_name, 'id': 0})
    else:
        return await update.message.reply_text("❤️ Kisi ke message pe reply karo ya naam likho jiske sath Dil Match karna hai!")

    if target.id == user.id:
        return await update.message.reply_text("🤨 Khud se hi kitna pyaar karoge? Kisi aur ka naam lo! 😂")

    # Percentage logic
    percentage = random.randint(1, 100)
    
    # Suspense Animation
    msg = await update.message.reply_text(f"💓 {user.first_name} aur {target.first_name} ka Dil Match ho raha hai...")
    await asyncio.sleep(1.5)
    await msg.edit_text("💘 Kundli milayi ja rahi hai...")
    await asyncio.sleep(1.5)

    # Result Shayaris
    if percentage > 90:
        status = "🔥 Rab Ne Bana Di Jodi! Ek dum Perfect Match! 😍"
    elif percentage > 70:
        status = "💖 Bohot gehra ishq hai! Bas shaadi ki deri hai. ✨"
    elif percentage > 40:
        status = "📈 Hmm, koshish jaari rakho, baat ban sakti hai. 😉"
    else:
        status = "💀 Rehne do beta, tumse na ho payega. Sirf dosti hi kaafi hai! 😂"

    final_text = (
        f"❤️ **DIL MATCH RESULT** ❤️\n\n"
        f"👤 {user.first_name}\n"
        f"👤 {target.first_name}\n\n"
        f"📊 **Compatibility:** {percentage}%\n"
        f"✨ **Angel says:** {status}"
    )
    
    await msg.edit_text(final_text)
