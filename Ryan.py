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
# INTERNAL SETUP (Logging & Environment)
# ======================================================
os.environ["GIT_PYTHON_REFRESH"] = "quiet"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Directory check for AI/Downloads
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# Loop policy for Windows/Linux servers
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ======================================================
# INTERNAL IMPORTS
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
# FLASK SERVER (Keep Alive)
# ======================================================
app = Flask(__name__)

@app.route('/')
def health():
    return f"{BOT_NAME} Angel is Online & Active! 💎"

def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# ======================================================
# POST INIT (Menu & Startup)
# ======================================================
async def post_init(application):
    await application.bot.set_my_commands([
        ("start", "🌸 Main Menu"),
        ("bal", "👛 Wallet"),
        ("battle", "⚔️ Couple Battle"),
        ("propose", "🌹 Propose"),
        ("couplestatus", "💑 Relationship Status"),
        ("premium", "💎 Buy Premium Plans"),
        ("apply_premium", "📩 Submit Payment ID"),
        ("truth", "💗 Truth"),
        ("dare", "🔥 Dare"),
        ("ping", "📶 Speed Check")
    ])
    bot_info = await application.bot.get_me()
    await log_to_channel(application.bot, "start", {"action": f"{BOT_NAME} Online! 🚀"})

# ======================================================
# MAIN EXECUTION
# ======================================================
if __name__ == '__main__':

    # Start Flask Server
    Thread(target=run_flask, daemon=True).start()

    # Request Config
    t_request = HTTPXRequest(connection_pool_size=25, connect_timeout=60, read_timeout=60)

    # Build Application
    app_bot = (
        ApplicationBuilder()
        .token(TOKEN)
        .request(t_request)
        .post_init(post_init)
        .build()
    )

    # --- 1. CORE HANDLERS ---
    app_bot.add_handler(CommandHandler("start", start.start))
    app_bot.add_handler(CommandHandler("help", start.help_command))
    app_bot.add_handler(CommandHandler("ping", ping.ping))

    # --- 2. ECONOMY & SHOP ---
    app_bot.add_handler(CommandHandler("bal", economy.balance))
    app_bot.add_handler(CommandHandler("daily", daily.daily_reward))
    app_bot.add_handler(CommandHandler("shop", shop.shop_menu))
    app_bot.add_handler(CallbackQueryHandler(shop.shop_callback, pattern="^shop_"))

    # --- 3. PREMIUM APPROVAL SYSTEM ---
    app_bot.add_handler(CommandHandler("premium", premium.premium_menu))
    app_bot.add_handler(CommandHandler("apply_premium", premium.apply_premium))
    app_bot.add_handler(CallbackQueryHandler(premium.premium_callback, pattern="^prem_"))

    # --- 4. COUPLE SYSTEM (BATTLE & ROOM) ---
    app_bot.add_handler(CommandHandler("battle", couple_battle.couple_battle))
    app_bot.add_handler(CommandHandler("battlelb", couple_battle.battle_lb))
    app_bot.add_handler(CommandHandler("propose", couple_room.propose))
    app_bot.add_handler(CommandHandler("accept", couple_room.accept_proposal))
    app_bot.add_handler(CommandHandler("couplestatus", couple_room.couple_status))

    # --- 5. FUN & GAMES ---
    app_bot.add_handler(CommandHandler("truth", couple_games.truth))
    app_bot.add_handler(CommandHandler("dare", couple_games.dare))
    app_bot.add_handler(CommandHandler("quiz", couple_games.quiz))
    app_bot.add_handler(CommandHandler("waifu", waifu.waifu))

    # --- 6. CHATBOT SETTINGS ---
    app_bot.add_handler(CommandHandler("chaton", chatbot.chaton))
    app_bot.add_handler(CommandHandler("chatoff", chatbot.chatoff))

    # --- 7. AUTO REPLY LOGIC ---
    # Group 3: Wishes (Sabse Pehle)
    app_bot.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, wishes.wish_handler),
        group=3
    )
    # Group 4: AI Reply & Stickers
    app_bot.add_handler(
        MessageHandler(
            (filters.TEXT | filters.Sticker.ALL) & ~filters.COMMAND,
            chatbot.ai_message_handler
        ),
        group=4
    )

    print(f"🔥 {BOT_NAME} is fully loaded with Premium Approval System!")
    app_bot.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
