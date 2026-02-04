import logging
from threading import Thread
from flask import Flask
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, filters
)
from telegram.request import HTTPXRequest

# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.INFO)

# ---------------- CONFIG ----------------
from baka.config import TOKEN, PORT, BOT_NAME

# ---------------- PLUGINS ----------------
from baka.plugins import (
    admin,
    ai_media,
    antispam,
    breakup,
    broadcast,
    chatbot,
    collection,
    couple_battle,
    couple_games,
    daily,
    economy,
    events,
    exclusive,
    flirt_mode,
    fun,
    game,
    jealous,
    love_match,
    mafia,
    marriage,
    moderation,
    ping,
    premium,
    riddle,
    shop,
    social,
    start,
    waifu,
    welcome,
    wishes,
    nsfw   # ✅ ADDED
)

# ---------------- KEEP ALIVE SERVER ----------------
app = Flask(__name__)

@app.route("/")
def home():
    return f"✨ {BOT_NAME} Engine is Online 🚀"

def run():
    app.run(host="0.0.0.0", port=PORT)


# ---------------- BOT COMMANDS ----------------
async def post_init(application):
    await application.bot.set_my_commands([
        ("start", "Start Bot"),
        ("ping", "Speed Check"),
        ("premium", "Premium Plans"),
        ("marry", "Propose"),
        ("match", "Love Match"),
        ("nsfw", "NSFW On/Off")  # ✅ ADDED
    ])


# ================= MAIN =================
if __name__ == "__main__":

    Thread(target=run, daemon=True).start()

    bot = (
        ApplicationBuilder()
        .token(TOKEN)
        .request(HTTPXRequest(connection_pool_size=30))
        .post_init(post_init)
        .build()
    )

    # ================= CORE =================
    bot.add_handler(CommandHandler("start", start.start))
    bot.add_handler(CommandHandler("ping", ping.ping))
    bot.add_handler(CommandHandler("welcome", welcome.welcome_command))


    # ================= ADMIN =================
    bot.add_handler(CommandHandler("broadcast", broadcast.broadcast))
    bot.add_handler(CommandHandler("ban", moderation.ban_user))
    bot.add_handler(CommandHandler("mute", moderation.mute_user))
    bot.add_handler(CommandHandler("unmute", moderation.unmute_user))
    bot.add_handler(CommandHandler("kick", moderation.kick_user))  # ✅ ADDED
    bot.add_handler(CommandHandler("admin", admin.admin_panel))


    # ================= NSFW CONTROL =================
    bot.add_handler(CommandHandler("nsfw", nsfw.toggle_nsfw))  # ✅ ADDED


    # ================= PREMIUM =================
    bot.add_handler(CommandHandler("premium", premium.premium_plans))
    bot.add_handler(CommandHandler("myplan", premium.check_plan))
    bot.add_handler(CommandHandler("approve", premium.approve_user))


    # ================= SOCIAL =================
    bot.add_handler(CommandHandler("marry", marriage.marry))
    bot.add_handler(CommandHandler("match", love_match.love_match))
    bot.add_handler(CommandHandler("waifu", waifu.waifu_handler))
    bot.add_handler(CommandHandler(["hug", "kiss", "slap"], exclusive.premium_action))
    bot.add_handler(CommandHandler("flirtmode", flirt_mode.flirt_toggle))
    bot.add_handler(CommandHandler("jealous", jealous.jealous_toggle))
    bot.add_handler(CommandHandler("breakup", breakup.breakup_toggle))


    # ================= GAMES =================
    bot.add_handler(CommandHandler("game", game.game_cmd))
    bot.add_handler(CommandHandler("mafia", mafia.mafia_game))
    bot.add_handler(CommandHandler("riddle", riddle.riddle_cmd))
    bot.add_handler(CommandHandler("daily", daily.daily_reward))
    bot.add_handler(CommandHandler("fun", fun.fun_cmd))
    bot.add_handler(CommandHandler("battle", couple_battle.start_battle))
    bot.add_handler(CommandHandler("couplegame", couple_games.start_game))


    # ================= ECONOMY =================
    bot.add_handler(CommandHandler("shop", shop.shop_cmd))
    bot.add_handler(CommandHandler("balance", economy.balance))
    bot.add_handler(CommandHandler("collect", collection.collect_cmd))


    # ================= AI & MEDIA =================
    bot.add_handler(MessageHandler(filters.PHOTO, ai_media.ai_media_handler))


    # ================= SECURITY (EARLY GROUP) =================
    bot.add_handler(MessageHandler(filters.Entity("url"), antispam.link_guard), group=1)

    # ✅ NSFW media delete (photo/video/gif/sticker)
    bot.add_handler(
        MessageHandler(
            filters.PHOTO |
            filters.VIDEO |
            filters.ANIMATION |
            filters.Sticker.ALL,
            nsfw.delete_nsfw_content
        ),
        group=2
    )


    # ================= CHATBOT =================
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, wishes.wish_handler), group=3)
    bot.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, chatbot.ai_message_handler), group=4)


    print(f"🚀 {BOT_NAME} started successfully...")
    bot.run_polling(drop_pending_updates=True)
