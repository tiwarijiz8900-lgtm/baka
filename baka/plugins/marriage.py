import asyncio
from telegram import Update
from telegram.ext import ContextTypes

# Temporary storage for proposals
PROPOSALS = {}

async def marry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    if not update.message.reply_to_message:
        return await update.message.reply_text("💍 Jisse shadi karni hai, uske message pe reply karke `/marry` likho!")

    target = update.message.reply_to_message.from_user

    if target.id == user.id:
        return await update.message.reply_text("🤨 Khud se shadi? Itne bure din aa gaye kya? 😂")

    PROPOSALS[target.id] = user.id
    
    await update.message.reply_text(
        f"💍 **PROPOSAL ALERT!** 💍\n\n"
        f"Hey {target.first_name}, {user.first_name} ne aapko shadi ke liye propose kiya hai! ❤️\n\n"
        f"Kya aapko ye kabool hai? (Reply karein `/accept_shadi` ya `/reject_shadi`)"
    )

async def accept_shadi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    if user.id not in PROPOSALS:
        return await update.message.reply_text("❌ Aapke paas koi proposal nahi aaya hai abhi.")

    partner_id = PROPOSALS.pop(user.id)
    partner_name = (await context.bot.get_chat(partner_id)).first_name

    # Animation
    msg = await update.message.reply_text("🎊 Band-baaja taiyar ho raha hai... 🥁")
    await asyncio.sleep(2)
    await msg.edit_text("🔥 Pheron ki taiyari ho rahi hai... 🕯️")
    await asyncio.sleep(2)

    certificate = (
        f"📜 **MARRIAGE CERTIFICATE** 📜\n\n"
        f"❤️ **Husband/Wife:** {partner_name}\n"
        f"❤️ **Husband/Wife:** {user.first_name}\n\n"
        f"✨ **Status:** Officially Married! ✨\n"
        f"📅 **Date:** 2026-02-02\n\n"
        f"Mubarak ho! Ab aap dono ek dusre ko pareshan karne ke liye officially legal ho! 😂🎉"
    )
    
    await msg.edit_text(certificate)
