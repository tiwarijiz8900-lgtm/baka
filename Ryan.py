import os
import logging
import asyncio
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram.request import HTTPXRequest

# PLUGINS IMPORT
from baka.config import TOKEN, PORT
from baka.plugins import (
    admin, ai_media, antispam, breakup, broadcast, chatbot, 
    collection, couple_battle, couple_games, daily, economy, 
    events, exclusive, flirt_mode, fun, game, jealous, 
    love_match, mafia, marriage, moderation, ping, premium, 
    riddle, shop, social, start, waifu, welcome, wishes
)

# FLASK SERVER FOR HEROKU
app = Flask(__name__)
@app.route('/')
def health(): return "✨ Angel Master is Live on Heroku!"

def run_flask():
    app.run(host='0.0.0.0', port=PORT)

if __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()
    
    # Building the App
    app_bot = ApplicationBuilder().token(TOKEN).request(HTTPXRequest(connection_pool_size=30)).build()

    # --- REGISTERING ALL HANDLERS ---
    # Security & Admin
    app_bot.add_handler(CommandHandler("ban", moderation.ban_user))
    app_bot.add_handler(CommandHandler("mute", moderation.mute_user))
    app_bot.add_handler(MessageHandler(filters.Entity("url"), antispam.link_guard), group=1)

    # Economy & Games
    app_bot.add_handler(CommandHandler(["bal", "profile"], economy.balance))
    app_bot.add_handler(CommandHandler("daily", daily.daily_reward))
    app_bot.add_handler(CommandHandler("shop", shop.shop_menu))
    app_bot.add_handler(CommandHandler("rob", mafia.rob_bank))
    app_bot.add_handler(CommandHandler("battle", couple_battle.couple_battle))

    # Marriage & Social
    app_bot.add_handler(CommandHandler("marry", marriage.marry))
    app_bot.add_handler(CommandHandler("accept_shadi", marriage.accept_shadi))
    app_bot.add_handler(CommandHandler("match", love_match.love_match))
    app_bot.add_handler(CommandHandler(["hug", "kiss"], exclusive.premium_action))

    # AI & Auto Replies
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, wishes.wish_handler), group=3)
    app_bot.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, chatbot.ai_message_handler), group=4)

    # Core
    app_bot.add_handler(CommandHandler("start", start.start))
    app_bot.add_handler(CommandHandler("ping", ping.ping))

    print("🚀 Bot is starting...")
    app_bot.run_polling(drop_pending_updates=True)
