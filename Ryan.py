import os
import logging
import asyncio
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters
)
from telegram.request import HTTPXRequest

# --- LOGGING SETUP ---
logging.basicConfig(level=logging.INFO)

# --- PLUGINS IMPORT ---
# Aapke screenshots ke hisaab se saare plugins yahan hain
from baka.config import TOKEN, PORT, BOT_NAME
from baka.plugins import (
    admin, ai_media, antispam, breakup, broadcast, chatbot, 
    collection, couple_battle, couple_games, daily, economy, 
    events, exclusive, flirt_mode, fun, game, jealous, 
    love_match, mafia, marriage, moderation, ping, premium, 
    riddle, shop, social, start, waifu, welcome, wishes
)

# --- FAST SERVER FOR HEROKU (Keep-Alive) ---
app = Flask(__name__)
@app.route('/')
def health(): return f"✨ {BOT_NAME} Engine is Online! 🚀"

def run_flask():
    app.run(host='0.0.0.0', port=PORT)

# --- BOT INITIALIZATION ---
async def post_init(application):
    await application.bot.set_my_commands([
        ("start", "🌸 Start Angel"),
        ("premium", "🌟 Plans & UPI"),
        ("myplan", "⏳ Check Validity"),
        ("approve", "✅ Admin Approval"),
        ("marry", "💍 Propose"),
        ("match", "❤️ Compatibility"),
        ("ping", "📶 Speed Check")
    ])

if __name__ == '__main__':
    # Threading Flask for Heroku
    Thread(target=run_flask, daemon=True).start()

    # App Build
    app_bot = (
        ApplicationBuilder()
        .token(TOKEN)
        .request(HTTPXRequest(connection_pool_size=30))
        .post_init(post_init)
        .build()
    )

    # --- HANDLERS INTEGRATION ---
    
    # Core & Admin
    app_bot.add_handler(CommandHandler("start", start.start))
    app_bot.add_handler(CommandHandler("ping", ping.ping))
    app_bot.add_handler(CommandHandler("broadcast", broadcast.broadcast))
    app_bot.add_handler(CommandHandler(["ban", "mute", "unmute"], [moderation.ban_user, moderation.mute_user, moderation.unmute_user]))

    # Premium & Subscription (Based on your new request)
    app_bot.add_handler(CommandHandler("premium", premium.premium_plans))
    app_bot.add_handler(CommandHandler("myplan", premium.check_plan))
    app_bot.add_handler(CommandHandler("approve", premium.approve_user))

    # Social & Fun
    app_bot.add_handler(CommandHandler("marry", marriage.marry))
    app_bot.add_handler(CommandHandler("match", love_match.love_match))
    app_bot.add_handler(CommandHandler("waifu", waifu.waifu_handler))
    app_bot.add_handler(CommandHandler(["hug", "kiss", "slap"], exclusive.premium_action))

    # Modes & AI
    app_bot.add_handler(CommandHandler("flirtmode", flirt_mode.flirt_toggle))
    app_bot.add_handler(CommandHandler("jealous", jealous.jealous_toggle))
    app_bot.add_handler(CommandHandler("breakup", breakup.breakup_toggle))

    # Auto Replies & Chatbot (Groq/Free AI)
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, wishes.wish_handler), group=3)
    app_bot.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, chatbot.ai_message_handler), group=4)

    # Security
    app_bot.add_handler(MessageHandler(filters.Entity("url"), antispam.link_guard), group=1)

    print(f"🚀 {BOT_NAME} is starting on Heroku...")
    app_bot.run_polling(drop_pending_updates=True)
