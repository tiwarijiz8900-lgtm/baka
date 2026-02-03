# Copyright (c) 2025 Telegram:- @WTF_Phantom
# Location: Supaul, Bihar

from pymongo import MongoClient
import certifi
from datetime import datetime, timedelta
from baka.config import MONGO_URI, REGISTER_BONUS


# ===============================
# 🔥 SAFE MONGO CONNECTION
# ===============================

if not MONGO_URI:
    raise RuntimeError("❌ MONGO_URI not found! Please set it in Heroku ENV")

RyanBaka = MongoClient(
    MONGO_URI,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000
)

db = RyanBaka["bakabot_db"]


# ===============================
# 🔥 COLLECTIONS
# ===============================

users_collection = db["users"]
groups_collection = db["groups"]
sudoers_collection = db["sudoers"]
chatbot_collection = db["chatbot"]
riddles_collection = db["riddles"]
premium_logs = db["premium_logs"]


# ===============================
# 🔥 USER MANAGEMENT
# ===============================

def ensure_user_exists(user):
    """Create user profile if not exists"""
    user_data = users_collection.find_one({"user_id": user.id})

    if not user_data:
        new_user = {
            "user_id": user.id,
            "username": user.username,
            "name": user.first_name,
            "balance": REGISTER_BONUS,
            "is_premium": False,
            "premium_expiry": None,
            "kills": 0,
            "status": "alive",
            "inventory": [],
            "partner_id": None,
            "registered_at": datetime.utcnow()
        }

        users_collection.insert_one(new_user)
        return new_user

    return user_data


# ===============================
# 🔥 PREMIUM SYSTEM
# ===============================

def add_premium_user(user_id, months):
    """Add / extend premium"""

    if months >= 999:
        expiry_date = datetime(2099, 12, 31)
    else:
        expiry_date = datetime.utcnow() + timedelta(days=30 * months)

    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {
            "is_premium": True,
            "premium_expiry": expiry_date
        }},
        upsert=True
    )

    return expiry_date


def check_premium(user_id):
    """Check premium validity"""

    user = users_collection.find_one({"user_id": user_id})

    if not user or not user.get("is_premium"):
        return False

    expiry = user.get("premium_expiry")

    if expiry and expiry < datetime.utcnow():
        users_collection.update_one(
            {"user_id": user_id},
            {"$set": {"is_premium": False}}
        )
        return False

    return True


# ===============================
# 🔥 SUDO SYSTEM
# ===============================

def is_sudo(user_id):
    return sudoers_collection.find_one({"user_id": user_id}) is not None


def add_sudo(user_id):
    if not is_sudo(user_id):
        sudoers_collection.insert_one({
            "user_id": user_id,
            "added_at": datetime.utcnow()
        })


# ===============================
# 🔥 GROUP TRACKING
# ===============================

def track_group(chat_id, title):
    if not groups_collection.find_one({"chat_id": chat_id}):
        groups_collection.insert_one({
            "chat_id": chat_id,
            "title": title,
            "claimed": False,
            "joined_at": datetime.utcnow()
        })
