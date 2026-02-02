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
# INTERNAL SETUP & LOGGING
# ======================================================
os.environ["GIT_PYTHON_REFRESH"] = "quiet"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

if not os.path.exists("downloads"):
    os.makedirs("downloads")

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ======================================================
# PLUGINS IMPORTS (Ensure these files exist)
# ======================================================
from baka.config import TOKEN, PORT
from baka.utils import log_to_channel, BOT_NAME

from baka.plugins import (
    start, economy, game, admin, broadcast, fun, events,
    welcome, ping, chatbot, riddle, social, ai_media,
    waifu, collection, shop, daily, couple_games, 
    wishes, couple_battle, couple_room, premium 
)

# ======================================================
# FLASK SERVER
# ======================================================
app = Flask(__name__)

@app.route('/')
def health():
    return f"✨ {BOT_NAME} Ultimate Engine is Live! 🚀"

def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# ======================================================
# BOT MENU (Commands List)
# ======================================================
async def post_init(application):
    await application.bot.set_my_commands([
        ("start", "🌸 Start Bot"),
        ("bal", "👛 Check Balance"),
        ("daily", "📅 Claim Daily"),
        ("pay", "💸 Send Coins"),
        ("top", "🏆 Leaderboard"),
        ("battle", "⚔️ Couple Fight"),
        ("battlelb", "🥇 Battle Board"),
        ("propose", "🌹 Propose Someone"),
        ("couplestatus", "💑 Love Info"),
        ("premium", "💎 VIP Plans"),
        ("apply_premium", "📩 Submit Payment"),
        ("truth", "💗 Truth Game"),
        ("dare", "🔥 Dare Game"),
        ("ping", "📶 Speed Check")
    ])
    print(f"✅ {BOT_NAME} All Systems Operational!")

# ======================================================
# MAIN BOT LOGIC
# ======================================================
if __name__ == '__main__':

    Thread(target=run_flask, daemon=True).start()

    # High-Performance Request Config
    t_request = HTTPXRequest(connection_pool_size=30, connect_timeout=60)

    app_bot = (
        ApplicationBuilder()
        .token(TOKEN)
        .request(t_request)
        .post_init(post_init)
        .build()
    )

    # --- 1. ADMIN & CORE ---
    app_bot.add_handler(CommandHandler("start", start.start))
    app_bot.add_handler(CommandHandler("ping", ping.ping))
    app_bot.add_handler(CommandHandler("broadcast", broadcast.broadcast))

    # --- 2. PREMIUM & APPROVAL (With MongoDB) ---
    app_bot.add_handler(CommandHandler("premium", premium.premium_menu))
    app_bot.add_handler(CommandHandler("apply_premium", premium.apply_premium))
    app_bot.add_handler(CallbackQueryHandler(premium.premium_callback, pattern="^prem_"))

    # --- 3. ECONOMY & GAMES ---
    app_bot.add_handler(CommandHandler("bal", economy.balance))
    app_bot.add_handler(CommandHandler("daily", daily.daily_reward))
    app_bot.add_handler(CommandHandler("pay", economy.pay))
    app_bot.add_handler(CommandHandler("top", economy.top_users))
    app_bot.add_handler(CommandHandler("gamble", game.gamble))
    app_bot.add_handler(CommandHandler("shop", shop.shop_menu))
    app_bot.add_handler(CallbackQueryHandler(shop.shop_callback, pattern="^shop_"))

    # --- 4. COUPLE SYSTEM (Room & Battle) ---
    app_bot.add_handler(CommandHandler("battle", couple_battle.couple_battle))
    app_bot.add_handler(CommandHandler("battlelb", couple_battle.battle_lb))
    app_bot.add_handler(CommandHandler("propose", couple_room.propose))
    app_bot.add_handler(CommandHandler("accept", couple_room.accept_proposal))
    app_bot.add_handler(CommandHandler("couplestatus", couple_room.couple_status))

    # --- 5. FUN & UNLIMITED GAMES ---
    app_bot.add_handler(CommandHandler("truth", couple_games.truth))
    app_bot.add_handler(CommandHandler("dare", couple_games.dare))
    app_bot.add_handler(CommandHandler("quiz", couple_games.quiz))

    # --- 6. AUTO HANDLERS (Priority Management) ---
    # Group 3: Wishes (GM/GN/Love Detect)
    app_bot.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, wishes.wish_handler),
        group=3
    )
    # Group 4: AI Chatbot Auto-Reply
    app_bot.add_handler(
        MessageHandler(
            (filters.TEXT | filters.Sticker.ALL) & ~filters.COMMAND,
            chatbot.ai_message_handler
        ),
        group=4
    )

    print(f"🚀 {BOT_NAME} Started Successfully with Premium & Economy!")
    app_bot.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
