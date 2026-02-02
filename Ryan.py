import os
os.environ["GIT_PYTHON_REFRESH"] = "quiet"

from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ChatMemberHandler, MessageHandler, filters
)
from telegram.request import HTTPXRequest

# ======================================================
# INTERNAL IMPORTS
# ======================================================
from baka.config import TOKEN, PORT
from baka.utils import log_to_channel, BOT_NAME

# All Plugins Imports
from baka.plugins import (
    start, economy, game, admin, broadcast, fun, events,
    welcome, ping, chatbot, riddle, social, ai_media,
    waifu, collection, shop, daily, couple_games, wishes # wishes plugin added
)

# ======================================================
# FLASK SERVER
# ======================================================
app = Flask(__name__)

@app.route('/')
def health():
    return "Baka Angel is Alive & Wishing! 🌸"

def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# ======================================================
# STARTUP MENU COMMANDS
# ======================================================
async def post_init(application):
    await application.bot.set_my_commands([
        ("start", "🌸 Main Menu"),
        ("help", "📖 Help Guide"),
        ("bal", "👛 Wallet"),
        ("daily", "📅 Daily Reward"),
        ("shop", "🛒 Shop"),
        ("pay", "💸 Send Money"),
        ("dice", "🎲 Game"),
        ("waifu", "👰 Get Waifu"),
        ("chaton", "💚 Chat ON"),
        ("chatoff", "🛑 Chat OFF"),
        ("truth", "💗 Truth Game"),
        ("dare", "🔥 Dare Game"),
        ("quiz", "🧠 Love Quiz"),
        ("ping", "📶 Speed")
    ])

    bot_info = await application.bot.get_me()
    await log_to_channel(application.bot, "start", {
        "user": "System",
        "chat": "Cloud",
        "action": f"{BOT_NAME} @{bot_info.username} Online 🚀"
    })

# ======================================================
# MAIN BOT ENGINE
# ======================================================
if __name__ == '__main__':

    Thread(target=run_flask, daemon=True).start()

    t_request = HTTPXRequest(
        connection_pool_size=25,
        connect_timeout=60.0,
        read_timeout=60.0
    )

    app_bot = (
        ApplicationBuilder()
        .token(TOKEN)
        .request(t_request)
        .post_init(post_init)
        .build()
    )

    # --- 1. BASIC & ADMIN HANDLERS ---
    app_bot.add_handler(CommandHandler("start", start.start))
    app_bot.add_handler(CommandHandler("help", start.help_command))
    app_bot.add_handler(CommandHandler("ping", ping.ping))

    # --- 2. ECONOMY HANDLERS ---
    app_bot.add_handler(CommandHandler("bal", economy.balance))
    app_bot.add_handler(CommandHandler("daily", daily.daily_reward))
    app_bot.add_handler(CommandHandler("shop", shop.shop_menu))
    if hasattr(economy, "pay"):
        app_bot.add_handler(CommandHandler("pay", economy.pay))
    app_bot.add_handler(CallbackQueryHandler(shop.shop_callback, pattern="^shop_"))

    # --- 3. CHATBOT & TAG COMMANDS ---
    app_bot.add_handler(CommandHandler("chaton", chatbot.chaton))
    app_bot.add_handler(CommandHandler("chatoff", chatbot.chatoff))
    app_bot.add_handler(CommandHandler("ask", chatbot.ask_ai))
    app_bot.add_handler(CommandHandler("chatbot", chatbot.chatbot_menu))
    app_bot.add_handler(CallbackQueryHandler(chatbot.chatbot_callback, pattern="^ai_"))

    # --- 4. COUPLE GAMES (UNLIMITED) ---
    app_bot.add_handler(CommandHandler("truth", couple_games.truth))
    app_bot.add_handler(CommandHandler("dare", couple_games.dare))
    app_bot.add_handler(CommandHandler("quiz", couple_games.quiz))

    # --- 5. AUTOMATIC WISHES (GM/GN/LOVE) ---
    # Group 3: Ye AI se pehle check hoga
    app_bot.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, wishes.wish_handler),
        group=3
    )

    # --- 6. 🔥 AI AUTO REPLY (Unlimited Angel Mode) ---
    # Group 4: Ye sabse last mein check hoga
    app_bot.add_handler(
        MessageHandler(
            (filters.TEXT | filters.Sticker.ALL) & ~filters.COMMAND,
            chatbot.ai_message_handler
        ),
        group=4
    )

    print("🔥 Baka Final: Economy + Wishes + AI Chat Running!")
    app_bot.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
