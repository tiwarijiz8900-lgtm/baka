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
# 🧩 PLUGINS IMPORTS
# ======================================================
from baka.config import TOKEN, PORT
from baka.utils import log_to_channel, BOT_NAME

from baka.plugins import (
    start, economy, game, admin, broadcast, ping, chatbot, 
    daily, couple_games, wishes, couple_battle, couple_room, 
    premium, exclusive, shop, breakup, jealous
)

# ======================================================
# 🌐 FLASK WEB SERVER
# ======================================================
app = Flask(__name__)

@app.route('/')
def health():
    return f"✨ {BOT_NAME} System is Online with Jealous Mode! 🚀"

def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# ======================================================
# 📜 BOT MENU
# ======================================================
async def post_init(application):
    await application.bot.set_my_commands([
        ("start", "🌸 Start Angel"),
        ("bal", "👛 Check Balance"),
        ("daily", "📅 Claim Coins"),
        ("premium", "💎 VIP Plans"),
        ("jealous", "🤨 Jealous Mode On/Off"),
        ("breakup", "💔 Breakup Mode On/Off"),
        ("battle", "⚔️ Couple Battle"),
        ("propose", "🌹 Propose"),
        ("top", "🏆 Richest Users"),
        ("ping", "📶 Speed Check")
    ])
    print(f"✅ {BOT_NAME} Master Engine Loaded!")

# ======================================================
# ⚙️ MAIN BOT ENGINE
# ======================================================
if __name__ == '__main__':

    Thread(target=run_flask, daemon=True).start()

    t_request = HTTPXRequest(connection_pool_size=30, connect_timeout=60)

    app_bot = (
        ApplicationBuilder()
        .token(TOKEN)
        .request(t_request)
        .post_init(post_init)
        .build()
    )

    # --- 1. CORE & MODERATION ---
    app_bot.add_handler(CommandHandler("start", start.start))
    app_bot.add_handler(CommandHandler("ping", ping.ping))
    app_bot.add_handler(CommandHandler("broadcast", admin.broadcast))

    # --- 2. ECONOMY & GLOBAL RANKING ---
    app_bot.add_handler(CommandHandler("bal", economy.balance))
    app_bot.add_handler(CommandHandler("daily", daily.daily_reward))
    app_bot.add_handler(CommandHandler("top", economy.top_users))
    app_bot.add_handler(CommandHandler("pay", economy.pay))
    app_bot.add_handler(CommandHandler("gamble", game.gamble))
    app_bot.add_handler(CommandHandler("shop", shop.shop_menu))
    app_bot.add_handler(CallbackQueryHandler(shop.shop_callback, pattern="^shop_"))

    # --- 3. PREMIUM, BREAKUP & JEALOUS MODES ---
    app_bot.add_handler(CommandHandler("premium", premium.premium_menu))
    app_bot.add_handler(CommandHandler("apply_premium", premium.apply_premium))
    app_bot.add_handler(CallbackQueryHandler(premium.premium_callback, pattern="^prem_"))
    app_bot.add_handler(CommandHandler("breakup", breakup.breakup_toggle))
    app_bot.add_handler(CommandHandler("jealous", jealous.jealous_toggle))

    # --- 4. COUPLE GAMES & VIP ACTIONS ---
    app_bot.add_handler(CommandHandler("battle", couple_battle.couple_battle))
    app_bot.add_handler(CommandHandler(["truth", "dare"], couple_games.truth_dare))
    app_bot.add_handler(CommandHandler(["hug", "kiss", "flirt"], exclusive.premium_action))

    # --- 5. COUPLE ROOM ---
    app_bot.add_handler(CommandHandler("propose", couple_room.propose))
    app_bot.add_handler(CommandHandler("accept", couple_room.accept_proposal))
    app_bot.add_handler(CommandHandler("couplestatus", couple_room.couple_status))

    # --- 6. AUTO HANDLERS (Priority Management) ---
    
    # Priority 1: Wishes (Group 3)
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

    print(f"🚀 {BOT_NAME} Started Successfully with Jealous Mode & Economy!")
    app_bot.run_polling(drop_pending_updates=True)
