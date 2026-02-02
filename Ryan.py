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

# --- LOGGING & SETUP ---
logging.basicConfig(level=logging.INFO)
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# --- ALL PLUGINS IMPORT (From your screenshots) ---
from baka.config import TOKEN, PORT
from baka.plugins import (
    admin, ai_media, antispam, breakup, broadcast, chatbot, 
    collection, couple_battle, couple_games, daily, economy, 
    events, exclusive, flirt_mode, fun, game, jealous, 
    love_match, mafia, marriage, moderation, ping, premium, 
    riddle, shop, social, start, waifu, welcome, wishes
)

# --- WEB SERVER FOR 24/7 ---
app = Flask(__name__)
@app.route('/')
def health(): return "✨ Angel Master Ultimate Engine is Online! 🚀"

def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# --- BOT COMMANDS MENU ---
async def post_init(application):
    await application.bot.set_my_commands([
        ("start", "🌸 Start Bot"),
        ("help", "📜 Help Menu"),
        ("bal", "👛 Check Balance"),
        ("marry", "💍 Propose"),
        ("rob", "💰 Rob Bank"),
        ("daily", "📅 Claim Reward"),
        ("shop", "🛒 Open Shop"),
        ("games", "🎮 Mini Games"),
        ("waifu", "👗 Get Waifu"),
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

    # --- 1. CORE & UTILITY HANDLERS ---
    app_bot.add_handler(CommandHandler("start", start.start))
    app_bot.add_handler(CommandHandler("ping", ping.ping))
    app_bot.add_handler(CommandHandler("broadcast", broadcast.broadcast))
    app_bot.add_handler(CommandHandler("events", events.show_events))

    # --- 2. SECURITY & ADMIN HANDLERS ---
    app_bot.add_handler(CommandHandler("ban", moderation.ban_user))
    app_bot.add_handler(CommandHandler("mute", moderation.mute_user))
    app_bot.add_handler(CommandHandler("unmute", moderation.unmute_user))
    app_bot.add_handler(CommandHandler("admin", admin.admin_panel))
    app_bot.add_handler(MessageHandler(filters.Entity("url"), antispam.link_guard), group=1)

    # --- 3. ECONOMY, SHOP & COLLECTION HANDLERS ---
    app_bot.add_handler(CommandHandler(["bal", "profile"], economy.balance))
    app_bot.add_handler(CommandHandler("daily", daily.daily_reward))
    app_bot.add_handler(CommandHandler("shop", shop.shop_menu))
    app_bot.add_handler(CommandHandler("collection", collection.show_collection))

    # --- 4. LOVE, MARRIAGE & SOCIAL HANDLERS ---
    app_bot.add_handler(CommandHandler("marry", marriage.marry))
    app_bot.add_handler(CommandHandler("accept_shadi", marriage.accept_shadi))
    app_bot.add_handler(CommandHandler("match", love_match.love_match))
    app_bot.add_handler(CommandHandler(["hug", "kiss", "slap", "lick"], exclusive.premium_action))
    app_bot.add_handler(CommandHandler("social", social.social_menu))

    # --- 5. GAMES, FUN & MEDIA HANDLERS ---
    app_bot.add_handler(CommandHandler("rob", mafia.rob_bank))
    app_bot.add_handler(CommandHandler("creategang", mafia.create_gang))
    app_bot.add_handler(CommandHandler("attack", mafia.attack_gang))
    app_bot.add_handler(CommandHandler("battle", couple_battle.couple_battle))
    app_bot.add_handler(CommandHandler("games", couple_games.games_menu))
    app_bot.add_handler(CommandHandler("riddle", riddle.get_riddle))
    app_bot.add_handler(CommandHandler("waifu", waifu.get_waifu))
    app_bot.add_handler(CommandHandler("fun", fun.fun_commands))
    app_bot.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, ai_media.media_handler))

    # --- 6. EMOTIONAL AI & MODES HANDLERS ---
    app_bot.add_handler(CommandHandler("flirtmode", flirt_mode.flirt_toggle))
    app_bot.add_handler(CommandHandler("jealous", jealous.jealous_toggle))
    app_bot.add_handler(CommandHandler("breakup", breakup.breakup_toggle))

    # --- 7. AUTO HANDLERS (AI & WISHES) ---
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, wishes.wish_handler), group=3)
    app_bot.add_handler(MessageHandler((filters.TEXT | filters.Sticker.ALL) & ~filters.COMMAND, chatbot.ai_message_handler), group=4)

    # --- 8. CALLBACK HANDLER (For Buttons) ---
    app_bot.add_handler(CallbackQueryHandler(premium.callback_handler)) # Example for all inline buttons

    print("🚀 ANGEL MASTER BOT IS FULLY LOADED WITH 30+ HANDLERS!")
    app_bot.run_polling(drop_pending_updates=True)
