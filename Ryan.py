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
# 🧩 PLUGINS IMPORTS (Ensure these files exist in baka/plugins/)
# ======================================================
from baka.config import TOKEN, PORT
from baka.utils import log_to_channel, BOT_NAME

from baka.plugins import (
    start, economy, game, admin, broadcast, ping, chatbot, 
    daily, couple_games, wishes, couple_battle, couple_room, 
    premium, exclusive, shop, breakup, jealous
)

# ======================================================
# 🌐 FLASK WEB SERVER (24/7 Hosting)
# ======================================================
app = Flask(__name__)

@app.route('/')
def health():
    return f"✨ {BOT_NAME} Ultimate System is Active! 🚀"

def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# ======================================================
# 📜 BOT MENU & COMMANDS
# ======================================================
async def post_init(application):
    await application.bot.set_my_commands([
        ("start", "🌸 Start Angel"),
        ("bal", "👛 Check Coins"),
        ("daily", "📅 Claim Daily Reward"),
        ("premium", "💎 VIP Plans"),
        ("apply_premium", "📩 Submit Payment"),
        ("battle", "⚔️ 1v1 Battle"),
        ("multibattle", "⚔️ 2v2 Team Battle"),
        ("breakup", "💔 Toggle Breakup Mode"),
        ("jealous", "🤨 Toggle Jealous Mode"),
        ("propose", "🌹 Propose Partner"),
        ("hug", "🫂 VIP Hug"),
        ("kiss", "💋 VIP Kiss"),
        ("top", "🏆 Global Leaderboard"),
        ("ping", "📶 Bot Speed")
    ])
    print(f"✅ {BOT_NAME} All Systems Loaded Successfully!")

# ======================================================
# ⚙️ MAIN BOT ENGINE
# ======================================================
if __name__ == '__main__':

    # Start Flask Web Server
    Thread(target=run_flask, daemon=True).start()

    # High-Performance Setup
    t_request = HTTPXRequest(connection_pool_size=30, connect_timeout=60)

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

    # --- 2. ECONOMY & RANKING ---
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

    # --- 4. EXCLUSIVE VIP ACTIONS ---
    app_bot.add_handler(CommandHandler(["hug", "kiss", "flirt"], exclusive.premium_action))

    # --- 5. BATTLE SYSTEM (1v1 & 2v2) ---
    app_bot.add_handler(CommandHandler("battle", couple_battle.couple_battle))
    app_bot.add_handler(CommandHandler("multibattle", couple_battle.multi_battle))
    app_bot.add_handler(CommandHandler("battlelb", couple_battle.battle_lb))

    # --- 6. COUPLE ROOM & GAMES ---
    app_bot.add_handler(CommandHandler("propose", couple_room.propose))
    app_bot.add_handler(CommandHandler("accept", couple_room.accept_proposal))
    app_bot.add_handler(CommandHandler("couplestatus", couple_room.couple_status))
    app_bot.add_handler(CommandHandler(["truth", "dare"], couple_games.truth_dare))

    # --- 7. AUTO-HANDLERS (Priority Wise) ---
    
    # Priority 1: Wishes (GM/GN/Hello) - Group 3
    app_bot.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, wishes.wish_handler),
        group=3
    )
    
    # Priority 2: AI Chatbot & Stickers - Group 4
    app_bot.add_handler(
        MessageHandler(
            (filters.TEXT | filters.Sticker.ALL) & ~filters.COMMAND,
            chatbot.ai_message_handler
        ),
        group=4
    )

    print(f"🚀 {BOT_NAME} is Live with Multi-Couple Battles & Global Economy!")
    app_bot.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
