# Copyright (c) 2025 Telegram:- @WTF_Phantom <DevixOP>

import os
import time

# ===============================
# 🔥 BASIC SETTINGS
# ===============================

START_TIME = time.time()

TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
PORT = int(os.environ.get("PORT", 8080)) # Heroku standard port


# --- FAST GROQ AI (Mistral Fix) ---
# Mistral ki jagah ab Groq use hoga jo super fast hai
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
AI_MODEL = "llama-3.1-70b-versatile"


# ===============================
# 🔥 PREMIUM & UPI SETTINGS
# ===============================

UPI_ID = os.getenv("UPI_ID", "ll_WTF_SHEZADA_ll@upi") 
UPI_QR_IMAGE = os.getenv("UPI_QR_IMAGE", "https://files.catbox.moe/wx05mx.jpg")

# Subscription Plans (INR)
PLAN_1_MONTH = 99
PLAN_1_YEAR = 899
PLAN_LIFETIME = 1499


# ===============================
# 🔥 Updater Config
# ===============================

UPSTREAM_REPO = os.getenv(
    "UPSTREAM_REPO",
    "https://github.com/tiwarijiz8900-lgtm/baka"
)

GIT_TOKEN = os.getenv("GIT_TOKEN", "")


# ===============================
# 🔥 Images & Links
# ===============================

START_IMG_URL = os.getenv(
    "START_IMG_URL",
    "https://files.catbox.moe/wx05mx.jpg"
)

HELP_IMG_URL = os.getenv(
    "HELP_IMG_URL",
    "https://files.catbox.moe/3r4ihh.jpg"
)

WELCOME_IMG_URL = os.getenv(
    "WELCOME_IMG_URL",
    "https://files.catbox.moe/wx05mx.jpg"
)

SUPPORT_GROUP = os.getenv(
    "SUPPORT_GROUP",
    "https://t.me/Love_Ki_Duniyaa"
)

SUPPORT_CHANNEL = os.getenv(
    "SUPPORT_CHANNEL",
    "https://t.me/Love_Bot_143"
)

OWNER_LINK = os.getenv(
    "OWNER_LINK",
    "https://t.me/ll_WTF_SHEZADA_ll"
)


# ===============================
# 🔥 IDs
# ===============================

try:
    LOGGER_ID = int(os.getenv("LOGGER_ID", "1003605595874").strip())
except:
    LOGGER_ID = 0

try:
    OWNER_ID = int(os.getenv("OWNER_ID", "0").strip())
except:
    OWNER_ID = 0

SUDO_IDS_STR = os.getenv("SUDO_IDS", "")


# ===============================
# 🔥 BOT INFO
# ===============================

BOT_NAME = "🫧 ᴀɴɢᴇʟ×͜࿐"


# ===============================
# 🔥 GAME CONSTANTS
# ===============================

REVIVE_COST = 500
PROTECT_1D_COST = 1000
PROTECT_2D_COST = 1800

REGISTER_BONUS = 5000
CLAIM_BONUS = 2000
RIDDLE_REWARD = 1000

DIVORCE_COST = 2000
WAIFU_PROPOSE_COST = 5000

TAX_RATE = 0.10
MARRIED_TAX_RATE = 0.05

AUTO_REVIVE_HOURS = 6
AUTO_REVIVE_BONUS = 200

ITEM_EXPIRY_HOURS = 24
MIN_CLAIM_MEMBERS = 100


# ===============================
# 🔥 SHOP ITEMS
# ===============================

SHOP_ITEMS = [
    {"id": "stick", "name": "🪵 Stick", "price": 500, "type": "weapon", "buff": 0.01},
    {"id": "knife", "name": "🔪 Knife", "price": 3500, "type": "weapon", "buff": 0.05},
    {"id": "bat", "name": "🏏 Bat", "price": 5000, "type": "weapon", "buff": 0.08},
    {"id": "axe", "name": "🪓 Axe", "price": 7500, "type": "weapon", "buff": 0.10},
    {"id": "pistol", "name": "🔫 Pistol", "price": 25000, "type": "weapon", "buff": 0.20},

    {"id": "paper", "name": "📰 Newspaper", "price": 500, "type": "armor", "buff": 0.01},
    {"id": "riot", "name": "🛡️ Riot Shield", "price": 40000, "type": "armor", "buff": 0.15},
    {"id": "diamond", "name": "💎 Diamond", "price": 200000, "type": "armor", "buff": 0.30},

    {"id": "rose", "name": "🌹 Rose", "price": 500, "type": "flex", "buff": 0},
    {"id": "ring", "name": "💍 Gold Ring", "price": 10000, "type": "flex", "buff": 0},
    {"id": "iphone", "name": "📱 iPhone 16 Pro", "price": 25000, "type": "flex", "buff": 0},
]
