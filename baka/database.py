# Copyright (c) 2025 Telegram:- @WTF_Phantom <DevixOP>
# Location: Supaul, Bihar 

from pymongo import MongoClient
import certifi
from datetime import datetime, timedelta
from baka.config import MONGO_URI, REGISTER_BONUS

# --- INITIALIZE CONNECTION ---
# tlsCAFile=certifi.where() ensures connection works on Heroku/Linux
RyanBaka = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = RyanBaka["bakabot_db"]

# --- DEFINING COLLECTIONS ---
users_collection = db["users"]       # Stores balance, premium status, stats
groups_collection = db["groups"]     # Tracks group settings & claim status
sudoers_collection = db["sudoers"]   # Stores admin/sudo IDs
chatbot_collection = db["chatbot"]   # Stores AI chat memory
riddles_collection = db["riddles"]   # Stores active riddles
premium_logs = db["premium_logs"]    # Tracks all /approve transactions

# --- USER MANAGEMENT FUNCTIONS ---

def ensure_user_exists(user):
    """Initializes user profile if not exists."""
    user_data = users_collection.find_one({"user_id": user.id})
    if not user_data:
        new_user = {
            "user_id": user.id,
            "username": user.username,
            "name": user.first_name,
            "balance": REGISTER_BONUS,
            "is_premium": False,
            "premium_expiry": None, # Format: datetime object
            "kills": 0,
            "status": "alive",
            "inventory": [],
            "partner_id": None,     # For Marriage System
            "registered_at": datetime.now()
        }
        users_collection.insert_one(new_user)
        return new_user
    return user_data

# --- PREMIUM SUBSCRIPTION LOGIC ---

def add_premium_user(user_id, months):
    """Adds or extends premium for a user."""
    # 999 months is treated as Lifetime
    if months >= 999:
        expiry_date = datetime(2099, 12, 31) # Practical lifetime
    else:
        expiry_date = datetime.now() + timedelta(days=30 * months)
    
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
    """Checks if user is currently premium and valid."""
    user = users_collection.find_one({"user_id": user_id})
    if not user or not user.get("is_premium"):
        return False
    
    # Auto-expiry check
    expiry = user.get("premium_expiry")
    if expiry and expiry < datetime.now():
        users_collection.update_one({"user_id": user_id}, {"$set": {"is_premium": False}})
        return False
    
    return True

# --- SUDO & ADMIN MANAGEMENT ---

def is_sudo(user_id):
    """Checks if user is in Sudoers list."""
    return sudoers_collection.find_one({"user_id": user_id}) is not None

def add_sudo(user_id):
    """Adds a new Sudo user."""
    if not is_sudo(user_id):
        sudoers_collection.insert_one({"user_id": user_id, "added_at": datetime.now()})

# --- GROUP TRACKING ---

def track_group(chat_id, title):
    """Ensures group is registered in DB."""
    if not groups_collection.find_one({"chat_id": chat_id}):
        groups_collection.insert_one({
            "chat_id": chat_id,
            "title": title,
            "claimed": False,
            "joined_at": datetime.now()
        })
