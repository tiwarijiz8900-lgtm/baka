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

# ⭐⭐⭐ COUPLE GAMES ADDED HERE ⭐⭐⭐
from baka.plugins import (
    start, economy, game, admin, broadcast, fun, events,
    welcome, ping, chatbot, riddle, social, ai_media,
    waifu, collection, shop, daily, couple_games
)

# ======================================================
# FLASK SERVER (Heroku/Render keep alive)
# ======================================================

app = Flask(__name__)

@app.route('/')
def health():
    return "Alive"


def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)


# ======================================================
# STARTUP MENU COMMANDS
# ======================================================

async def post_init(application):

    await application.bot.set_my_commands([

        ("start", "🌸 Menu"),
        ("help", "📖 Help"),

        ("bal", "👛 Wallet"),
        ("daily", "📅 Daily"),
        ("shop", "🛒 Shop"),

        ("dice", "🎲 Game"),
        ("draw", "🎨 AI Art"),

        # 🤖 Chatbot
        ("chatbot", "🧠 AI Settings"),
        ("chaton", "💚 Chat ON"),
        ("chatoff", "🛑 Chat OFF"),
        ("tagon", "🏷️ Tag ON"),
        ("tagoff", "❌ Tag OFF"),
        ("tagall", "📢 Tag All"),
        ("ask", "🤖 Ask AI"),

        # 💑 Couple Games ⭐⭐⭐
        ("truth", "💗 Truth Game"),
        ("dare", "🔥 Dare Game"),
        ("quiz", "🧠 Love Quiz"),
        ("couplegame", "💑 Random Couple Game"),

        ("ping", "📶 Ping")
    ])

    bot_info = await application.bot.get_me()

    await log_to_channel(application.bot, "start", {
        "user": "System",
        "chat": "Cloud",
        "action": f"{BOT_NAME} @{bot_info.username} Online 🚀"
    })


# ======================================================
# MAIN
# ======================================================

if __name__ == '__main__':

    Thread(target=run_flask, daemon=True).start()

    t_request = HTTPXRequest(
        connection_pool_size=16,
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

    # ======================================================
    # BASIC
    # ======================================================

    app_bot.add_handler(CommandHandler("start", start.start))
    app_bot.add_handler(CommandHandler("help", start.help_command))
    app_bot.add_handler(CommandHandler("ping", ping.ping))


    # ======================================================
    # 🤖 CHATBOT COMMANDS
    # ======================================================

    app_bot.add_handler(CommandHandler("chaton", chatbot.chaton))
    app_bot.add_handler(CommandHandler("chatoff", chatbot.chatoff))
    app_bot.add_handler(CommandHandler("tagon", chatbot.tagon))
    app_bot.add_handler(CommandHandler("tagoff", chatbot.tagoff))
    app_bot.add_handler(CommandHandler("tagall", chatbot.tagall))
    app_bot.add_handler(CommandHandler("ask", chatbot.ask_ai))
    app_bot.add_handler(CommandHandler("chatbot", chatbot.chatbot_menu))
    app_bot.add_handler(CallbackQueryHandler(chatbot.chatbot_callback, pattern="^ai_"))


    # ======================================================
    # 💑 COUPLE GAMES (UNLIMITED) ⭐⭐⭐
    # ======================================================

    app_bot.add_handler(CommandHandler("truth", couple_games.truth))
    app_bot.add_handler(CommandHandler("dare", couple_games.dare))
    app_bot.add_handler(CommandHandler("quiz", couple_games.quiz))

    # optional random mix game
    if hasattr(couple_games, "couplegame"):
        app_bot.add_handler(CommandHandler("couplegame", couple_games.couplegame))


    # ======================================================
    # 🔥 AI AUTO REPLY (UNLIMITED)
    # ======================================================

    app_bot.add_handler(
        MessageHandler(
            (filters.TEXT | filters.Sticker.ALL) & ~filters.COMMAND,
            chatbot.ai_message_handler
        ),
        group=4
    )

    print("🔥 Bot Running With AI + Unlimited Chatbot + Tag + Couple Games")
    app_bot.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
        )
