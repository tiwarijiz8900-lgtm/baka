import os
import logging
import asyncio
import platform
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters
)
from telegram.request import HTTPXRequest

# ======================================================
# 🛠️ INTERNAL SETUP & LOGGING
# ======================================================
os.environ["GIT_PYTHON_REFRESH"] = "quiet"
logging.basicConfig(level=logging.INFO)

if not os.path.exists("downloads"):
    os.makedirs("downloads")

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ======================================================
# 🧩 PLUGINS IMPORTS
# ======================================================
# Ensure these files exist in your baka/plugins/ folder
from baka.config import TOKEN, PORT
from baka.plugins import (
    start, economy, admin, broadcast, ping, chatbot, 
    daily, wishes, couple_battle, premium, exclusive, 
    breakup, jealous, flirt_mode, love_match, marriage, 
    mafia, antispam, moderation
)

# ======================================================
# 🌐 FLASK WEB SERVER (For 24/7 Hosting)
# ======================================================
app = Flask(__name__)

@app.route('/')
def health():
    return "✨ Angel Master Ultimate System is Online & Secured! 🛡️"

def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# ======================================================
# 📜 BOT MENU & COMMANDS
# ======================================================
async def post_init(application):
    await application.bot.set_my_commands([
        ("start", "🌸 Start Angel"),
        ("bal", "👛 Check Coins"),
        ("daily", "📅 Claim Daily Coins"),
        ("match", "❤️ Dil Match %"),
        ("marry", "💍 Propose Marriage"),
        ("rob", "💰 Rob a Bank"),
        ("attack", "⚔️ Attack Gang Vault"),
        ("ban", "🚀 Ban User (Admin Only)"),
        ("mute", "🤫 Mute User (Admin Only)"),
        ("flirtmode", "😘 Toggle Flirt AI"),
        ("jealous", "🤨 Toggle Jealousy"),
        ("breakup", "💔 Toggle Breakup"),
        ("top", "🏆 Global Ranking"),
        ("ping", "📶 Bot Speed Check")
    ])
    print("✅ All System Commands Registered!")

# ======================================================
# ⚙️ MAIN ENGINE START
# ======================================================
if __name__ == '__main__':

    # Start Flask in background
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

    # --- 1. SECURITY & MODERATION (High Priority) ---
    # Anti-Link Guard (Group 1)
    app_bot.add_handler(
        MessageHandler(filters.Entity("url") | filters.Entity("text_link"), antispam.link_guard), 
        group=1
    )
    # Admin Commands
    app_bot.add_handler(CommandHandler("ban", moderation.ban_user))
    app_bot.add_handler(CommandHandler("mute", moderation.mute_user))
    app_bot.add_handler(CommandHandler("unmute", moderation.unmute_user))

    # --- 2. ECONOMY & MAFIA SYSTEM ---
    app_bot.add_handler(CommandHandler(["bal", "top"], economy.balance))
    app_bot.add_handler(CommandHandler("daily", daily.daily_reward))
    app_bot.add_handler(CommandHandler("rob", mafia.rob_bank))
    app_bot.add_handler(CommandHandler("creategang", mafia.create_gang))
    app_bot.add_handler(CommandHandler("attack", mafia.attack_gang))

    # --- 3. LOVE, MARRIAGE & FUN ---
    app_bot.add_handler(CommandHandler("match", love_match.love_match))
    app_bot.add_handler(CommandHandler("marry", marriage.marry))
    app_bot.add_handler(CommandHandler("accept_shadi", marriage.accept_shadi))
    app_bot.add_handler(CommandHandler(["hug", "kiss", "flirt"], exclusive.premium_action))

    # --- 4. EMOTIONAL MODES ---
    app_bot.add_handler(CommandHandler("flirtmode", flirt_mode.flirt_toggle))
    app_bot.add_handler(CommandHandler("jealous", jealous.jealous_toggle))
    app_bot.add_handler(CommandHandler("breakup", breakup.breakup_toggle))

    # --- 5. UTILITY & CORE ---
    app_bot.add_handler(CommandHandler("start", start.start))
    app_bot.add_handler(CommandHandler("ping", ping.ping))
    app_bot.add_handler(CommandHandler("broadcast", broadcast.broadcast))

    # --- 6. AUTO HANDLERS (Priority Management) ---
    # Priority 1: Auto-Wishes (Group 3)
    app_bot.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, wishes.wish_handler),
        group=3
    )
    # Priority 2: AI Chatbot (Group 4)
    app_bot.add_handler(
        MessageHandler(
            (filters.TEXT | filters.Sticker.ALL) & ~filters.COMMAND,
            chatbot.ai_message_handler
        ),
        group=4
    )

    print("🚀 Baka Angel MASTER ENGINE is Live! (2026 Edition)")
    app_bot.run_polling(drop_pending_updates=True)
