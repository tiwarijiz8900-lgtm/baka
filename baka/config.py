# Copyright (c) 2025 Telegram:- @WTF_Phantom <DevixOP>

import os
import time

# ===============================
# 🔥 BASIC SETTINGS
# ===============================

START_TIME = time.time()

TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
PORT = int(os.environ.get("PORT", 5000))


# ===============================
# 🔥 AI SYSTEM (SambaNova Only)
# ===============================
# ❌ Mistral removed
# ✅ Only SambaNova

SAMBANOVA_API_KEY = os.getenv("SAMBANOVA_API_KEY", "")
SAMBANOVA_URL = "https://cloud.sambanova.ai/api/v1/chat/completions"
AI_MODEL = "Meta-Llama-3-8B-Instruct"


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
# 🔥 SHOP ITEMS (UNCHANGED)
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
