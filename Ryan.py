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

# --- SETUP LOGGING ---
logging.basicConfig(level=logging.INFO)

# --- PLUGINS IMPORT (As per your Screenshots) ---
from baka.config import TOKEN, PORT
from baka.plugins import (
    start, economy, daily, admin, moderation, antispam, 
    marriage, love_match, mafia, flirt_mode, jealous, 
    breakup, wishes, chatbot, couple_battle, couple_games,
    exclusive, premium, shop, ping, broadcast, fun, game
)

# --- FLASK SERVER ---
app = Flask(__name__)
@app.route('/')
def health(): return "✨ Angel Multi-Module Engine is Online! 🚀"

def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# --- COMMANDS REGISTRATION ---
async def post_init(application):
    await application.bot.set_my_commands([
        ("start", "🌸 Start Bot"),
        ("bal", "👛 Check Coins"),
        ("marry", "💍 Propose"),
        ("match", "❤️ Love Match"),
        ("rob", "💰 Rob Bank"),
        ("daily", "📅 Daily Reward"),
        ("shop", "🛒 Open Shop"),
        ("battle", "⚔️ Couple Battle"),
        ("games", "🎮 Mini Games"),
        ("ban", "🚀 Ban User"),
        ("ping", "📶 Speed Check")
    ])

if __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()

    app_bot = (
        ApplicationBuilder()
        .token(TOKEN)
        .request(HTTPXRequest(connection_pool_size=30))
        .post_init(post_init)
        .build()
    )

    # --- 1. SECURITY & ADMIN ---
    app_bot.add_handler(CommandHandler("ban", moderation.ban_user))
    app_bot.add_handler(CommandHandler("mute", moderation.mute_user))
    app_bot.add_handler(CommandHandler("broadcast", broadcast.broadcast))
    app_bot.add_handler(MessageHandler(filters.Entity("url"), antispam.link_guard), group=1)

    # --- 2. ECONOMY & SHOP ---
    app_bot.add_handler(CommandHandler(["bal", "profile"], economy.balance))
    app_bot.add_handler(CommandHandler("daily", daily.daily_reward))
    app_bot.add_handler(CommandHandler("shop", shop.shop_menu))
    app_bot.add_handler(CommandHandler("pay", economy.pay))

    # --- 3. MAFIA & GAMES ---
    app_bot.add_handler(CommandHandler("rob", mafia.rob_bank))
    app_bot.add_handler(CommandHandler("creategang", mafia.create_gang))
    app_bot.add_handler(CommandHandler("attack", mafia.attack_gang))
    app_bot.add_handler(CommandHandler("battle", couple_battle.couple_battle))
    app_bot.add_handler(CommandHandler("games", couple_games.games_menu))

    # --- 4. LOVE & SOCIAL ---
    app_bot.add_handler(CommandHandler("marry", marriage.marry))
    app_bot.add_handler(CommandHandler("accept_shadi", marriage.accept_shadi))
    app_bot.add_handler(CommandHandler("match", love_match.love_match))
    app_bot.add_handler(CommandHandler(["hug", "kiss", "slap"], exclusive.premium_action))

    # --- 5. MODES & AI ---
    app_bot.add_handler(CommandHandler("flirtmode", flirt_mode.flirt_toggle))
    app_bot.add_handler(CommandHandler("jealous", jealous.jealous_toggle))
    app_bot.add_handler(CommandHandler("breakup", breakup.breakup_toggle))

    # --- 6. UTILITY ---
    app_bot.add_handler(CommandHandler("start", start.start))
    app_bot.add_handler(CommandHandler("ping", ping.ping))

    # --- 7. AUTO HANDLERS ---
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, wishes.wish_handler), group=3)
    app_bot.add_handler(MessageHandler((filters.TEXT | filters.Sticker.ALL) & ~filters.COMMAND, chatbot.ai_message_handler), group=4)

    print("🚀 Sabhi Plugins Load Ho Chuke Hain! Bot Ready Hai.")
    app_bot.run_polling(drop_pending_updates=True)
