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
# 🛠️ SYSTEM SETUP & LOGGING
# ======================================================
logging.basicConfig(level=logging.INFO)
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ======================================================
# 🧩 ALL PLUGINS IMPORT (As per your Screenshot)
# ======================================================
from baka.config import TOKEN, PORT
from baka.plugins import (
    admin, ai_media, antispam, breakup, broadcast, chatbot, 
    collection, couple_battle, couple_games, daily, economy, 
    events, exclusive, flirt_mode, fun, game, jealous, 
    love_match, mafia, marriage, moderation, ping, premium, 
    riddle, shop, social, start, waifu, welcome, wishes
)

# ======================================================
# FLASK SERVER FOR HEROKU
# ======================================================
app = Flask(__name__)
@app.route('/')
def health(): return "✨ Angel Master is Live on Heroku!"! 🚀"

def run_flask():
    # Heroku PORT dynamically pick karta hai
    app.run(host='0.0.0.0', port=PORT)

# ======================================================
# 📜 AUTOMATIC COMMAND MENU (BotFather Ready)
# ======================================================
async def post_init(application):
    await application.bot.set_my_commands([
        ("start", "🌸 Start Bot"),
        ("help", "📜 Help Menu"),
        ("bal", "👛 Check Balance"),
        ("marry", "💍 Propose Marriage"),
        ("match", "❤️ Love Match"),
        ("rob", "💰 Rob a Bank"),
        ("battle", "⚔️ Couple Battle"),
        ("shop", "🛒 Item Shop"),
        ("daily", "📅 Claim Daily"),
        ("waifu", "👗 Get Waifu"),
        ("ban", "🚀 Ban (Admin)"),
        ("ping", "📶 Speed Check")
    ])

# ======================================================
# ⚙️ MAIN ENGINE & HANDLERS
# ======================================================
if __name__ == '__main__':
    # Flask in background
    Thread(target=run_flask, daemon=True).start()

    # Build Application
    t_request = HTTPXRequest(connection_pool_size=30)
    app_bot = (
        ApplicationBuilder()
        .token(TOKEN)
        .request(t_request)
        .post_init(post_init)
        .build()
    )

    # --- 1. CORE & ADMIN HANDLERS ---
    app_bot.add_handler(CommandHandler("start", start.start))
    app_bot.add_handler(CommandHandler("ping", ping.ping))
    app_bot.add_handler(CommandHandler("broadcast", broadcast.broadcast))
    app_bot.add_handler(CommandHandler(["ban", "mute", "unmute"], [moderation.ban_user, moderation.mute_user, moderation.unmute_user]))
    app_bot.add_handler(MessageHandler(filters.Entity("url"), antispam.link_guard), group=1)

    # --- 2. ECONOMY & SHOP HANDLERS ---
    app_bot.add_handler(CommandHandler(["bal", "profile"], economy.balance))
    app_bot.add_handler(CommandHandler("daily", daily.daily_reward))
    app_bot.add_handler(CommandHandler("shop", shop.shop_menu))
    app_bot.add_handler(CommandHandler("collection", collection.show_collection))
    app_bot.add_handler(CommandHandler("top", economy.top_users))

    # --- 3. MAFIA & GAMES HANDLERS ---
    app_bot.add_handler(CommandHandler(["rob", "attack"], [mafia.rob_bank, mafia.attack_gang]))
    app_bot.add_handler(CommandHandler("creategang", mafia.create_gang))
    app_bot.add_handler(CommandHandler("battle", couple_battle.couple_battle))
    app_bot.add_handler(CommandHandler("games", couple_games.games_menu))
    app_bot.add_handler(CommandHandler("waifu", waifu.get_waifu))
    app_bot.add_handler(CommandHandler("riddle", riddle.get_riddle))

    # --- 4. LOVE & MARRIAGE HANDLERS ---
    app_bot.add_handler(CommandHandler("marry", marriage.marry))
    app_bot.add_handler(CommandHandler("accept_shadi", marriage.accept_shadi))
    app_bot.add_handler(CommandHandler("match", love_match.love_match))
    app_bot.add_handler(CommandHandler(["hug", "kiss", "slap", "lick"], exclusive.premium_action))

    # --- 5. MODES & EMOTIONAL AI ---
    app_bot.add_handler(CommandHandler("flirtmode", flirt_mode.flirt_toggle))
    app_bot.add_handler(CommandHandler("jealous", jealous.jealous_toggle))
    app_bot.add_handler(CommandHandler("breakup", breakup.breakup_toggle))

    # --- 6. AUTO HANDLERS (Wishes & Chatbot) ---
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, wishes.wish_handler), group=3)
    app_bot.add_handler(
        MessageHandler((filters.TEXT | filters.Sticker.ALL) & ~filters.COMMAND, chatbot.ai_message_handler), 
        group=4
    )

    # --- 7. CALLBACKS (For Buttons) ---
    app_bot.add_handler(CallbackQueryHandler(premium.callback_handler))

    print("🚀 ANGEL MASTER ENGINE: FULLY LOADED & READY!")
    app_bot.run_polling(drop_pending_updates=True)
