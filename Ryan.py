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

# --- LOGGING ---
logging.basicConfig(level=logging.INFO)

# --- PLUGINS IMPORT ---
from baka.config import TOKEN, PORT
from baka.plugins import (
    admin, ai_media, antispam, breakup, broadcast, chatbot, 
    collection, couple_battle, couple_games, daily, economy, 
    events, exclusive, flirt_mode, fun, game, jealous, 
    love_match, mafia, marriage, moderation, ping, premium, 
    riddle, shop, social, start, waifu, welcome, wishes
)

# --- WEB SERVER FOR HEROKU ---
app = Flask(__name__)
@app.route('/')
def health(): return "✨ Angel Master Economy System is Online! 🚀"

def run_flask():
    app.run(host='0.0.0.0', port=PORT)

# --- BOT COMMANDS SETTING ---
async def post_init(application):
    await application.bot.set_my_commands([
        ("register", "🔑 Create Wallet"),
        ("bal", "👛 Wallet & Profile"),
        ("give", "💸 Send Coins to Friend"),
        ("top", "🏆 Leaderboard"),
        ("claim", "💎 Group Bonus"),
        ("marry", "💍 Propose"),
        ("rob", "💰 Bank Robbery"),
        ("shop", "🛒 Item Shop"),
        ("help", "📜 Help Menu")
    ])

if __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()

    # Application Build
    app_bot = (
        ApplicationBuilder()
        .token(TOKEN)
        .request(HTTPXRequest(connection_pool_size=30))
        .post_init(post_init)
        .build()
    )

    # --- 1. CORE & START ---
    app_bot.add_handler(CommandHandler("start", start.start))
    app_bot.add_handler(CommandHandler("help", start.start)) # Using start as help placeholder

    # --- 2. ECONOMY SYSTEM (As per your code) ---
    app_bot.add_handler(CommandHandler("register", economy.register))
    app_bot.add_handler(CommandHandler("claim", economy.claim))
    app_bot.add_handler(CommandHandler(["bal", "balance", "profile"], economy.balance))
    app_bot.add_handler(CommandHandler(["top", "ranking"], economy.ranking))
    app_bot.add_handler(CommandHandler(["give", "pay"], economy.give))
    
    # Callback for Inventory View
    app_bot.add_handler(CallbackQueryHandler(economy.inventory_callback, pattern="^inv_view\|"))

    # --- 3. MAFIA & CRIME ---
    app_bot.add_handler(CommandHandler("rob", mafia.rob_bank))
    app_bot.add_handler(CommandHandler("creategang", mafia.create_gang))
    app_bot.add_handler(CommandHandler("attack", mafia.attack_gang))

    # --- 4. LOVE & MARRIAGE ---
    app_bot.add_handler(CommandHandler("marry", marriage.marry))
    app_bot.add_handler(CommandHandler("accept_shadi", marriage.accept_shadi))
    app_bot.add_handler(CommandHandler("match", love_match.love_match))

    # --- 5. GAMES & FUN ---
    app_bot.add_handler(CommandHandler("battle", couple_battle.couple_battle))
    app_bot.add_handler(CommandHandler("waifu", waifu.get_waifu))
    app_bot.add_handler(CommandHandler("riddle", riddle.get_riddle))
    app_bot.add_handler(CommandHandler("shop", shop.shop_menu))

    # --- 6. SECURITY & ADMIN ---
    app_bot.add_handler(CommandHandler("ban", moderation.ban_user))
    app_bot.add_handler(CommandHandler("mute", moderation.mute_user))
    app_bot.add_handler(MessageHandler(filters.Entity("url"), antispam.link_guard), group=1)

    # --- 7. AUTO HANDLERS ---
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, wishes.wish_handler), group=3)
    app_bot.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, chatbot.ai_message_handler), group=4)

    print("🚀 ANGEL MASTER BOT START SUCCESSFULLY!")
    app_bot.run_polling(drop_pending_updates=True)
