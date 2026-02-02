import os
import logging
import asyncio
import platform
import random
from datetime import datetime
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters
)
from telegram.request import HTTPXRequest

# ======================================================
# 🛠️ SETUP & LOGGING
# ======================================================
logging.basicConfig(level=logging.INFO)
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ======================================================
# 🧩 PLUGINS IMPORTS
# ======================================================
from baka.config import TOKEN, PORT
from baka.plugins import (
    start, economy, daily, admin, moderation, 
    antispam, marriage, love_match, mafia, flirt_mode, 
    jealous, breakup, wishes, chatbot, help as help_plugin
)

# ======================================================
# 🌐 WEB SERVER (For 24/7 Hosting)
# ======================================================
app = Flask(__name__)
@app.route('/')
def health(): return "✨ Angel Master Pro v4.0 is Active & Online! 🚀"

def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# ======================================================
# ⚙️ MAIN BOT ENGINE
# ======================================================
async def post_init(application):
    # Bot menu mein saari commands ek sath set karna
    await application.bot.set_my_commands([
        ("start", "🌸 Start Bot"),
        ("help", "📜 Help Menu"),
        ("bal", "👛 Wallet Balance"),
        ("daily", "📅 Claim Daily Reward"),
        ("top", "🏆 Global Leaderboard"),
        ("pay", "💸 Transfer Coins"),
        ("marry", "💍 Propose Marriage"),
        ("match", "❤️ Dil Match %"),
        ("rob", "💰 Rob a Bank"),
        ("creategang", "🔥 Create Mafia Gang"),
        ("attack", "⚔️ Attack Gang Vault"),
        ("flirtmode", "😘 Toggle Flirt AI"),
        ("jealous", "🤨 Toggle Jealousy"),
        ("breakup", "💔 Toggle Breakup"),
        ("ban", "🚀 Ban User (Admin)"),
        ("mute", "🤫 Mute User (Admin)"),
        ("ping", "📶 Speed Check")
    ])

if __name__ == '__main__':
    # Start Web Server
    Thread(target=run_flask, daemon=True).start()

    # Build Application
    t_request = HTTPXRequest(connection_pool_size=30, connect_timeout=60)
    app_bot = (
        ApplicationBuilder()
        .token(TOKEN)
        .request(t_request)
        .post_init(post_init)
        .build()
    )

    # --- 1. CORE & HELP SYSTEM ---
    app_bot.add_handler(CommandHandler("start", start.start))
    app_bot.add_handler(CommandHandler("help", help_plugin.help_command))
    app_bot.add_handler(CallbackQueryHandler(help_plugin.help_callback, pattern="^help_"))
    app_bot.add_handler(CommandHandler("ping", ping.ping))

    # --- 2. SECURITY & MODERATION (Group 1) ---
    app_bot.add_handler(CommandHandler("ban", moderation.ban_user))
    app_bot.add_handler(CommandHandler("mute", moderation.mute_user))
    app_bot.add_handler(CommandHandler("unmute", moderation.unmute_user))
    app_bot.add_handler(
        MessageHandler(filters.Entity("url") | filters.Entity("text_link"), antispam.link_guard), 
        group=1
    )

    # --- 3. TOTAL ECONOMY SYSTEM ---
    app_bot.add_handler(CommandHandler(["bal", "profile"], economy.balance))
    app_bot.add_handler(CommandHandler("daily", daily.daily_reward))
    app_bot.add_handler(CommandHandler("top", economy.top_users))
    app_bot.add_handler(CommandHandler("pay", economy.pay))

    # --- 4. MAFIA & CRIME ---
    app_bot.add_handler(CommandHandler("rob", mafia.rob_bank))
    app_bot.add_handler(CommandHandler("creategang", mafia.create_gang))
    app_bot.add_handler(CommandHandler("attack", mafia.attack_gang))
    app_bot.add_handler(CommandHandler("ganginfo", mafia.gang_info))

    # --- 5. LOVE & MARRIAGE SYSTEM ---
    app_bot.add_handler(CommandHandler("match", love_match.love_match))
    app_bot.add_handler(CommandHandler("marry", marriage.marry))
    app_bot.add_handler(CommandHandler("accept_shadi", marriage.accept_shadi))

    # --- 6. EMOTIONAL AI MODES ---
    app_bot.add_handler(CommandHandler("flirtmode", flirt_mode.flirt_toggle))
    app_bot.add_handler(CommandHandler("jealous", jealous.jealous_toggle))
    app_bot.add_handler(CommandHandler("breakup", breakup.breakup_toggle))

    # --- 7. AUTO HANDLERS (Wishes & Chatbot) ---
    app_bot.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, wishes.wish_handler), 
        group=3
    )
    app_bot.add_handler(
        MessageHandler((filters.TEXT | filters.Sticker.ALL) & ~filters.COMMAND, chatbot.ai_message_handler), 
        group=4
    )

    print("🚀 ANGEL MASTER BOT: FULL ECONOMY + MAFIA + MARRIAGE VERSION IS LIVE!")
    app_bot.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
