# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Fixes by Gemini AI for ZEXX

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatType
from baka.config import REGISTER_BONUS, OWNER_ID, TAX_RATE, CLAIM_BONUS, MARRIED_TAX_RATE, SHOP_ITEMS, MIN_CLAIM_MEMBERS
from baka.utils import ensure_user_exists, get_mention, format_money, resolve_target, log_to_channel, stylize_text, track_group
from baka.database import users_collection, groups_collection
from baka.plugins.chatbot import get_groq_response 

# --- SHARED UTILS FOR OTHER PLUGINS ---
async def get_balance(user_id: int):
    """Directly fetch balance for Battle/Premium plugins"""
    user = users_collection.find_one({"user_id": user_id})
    return user.get("balance", 0) if user else 0

async def update_balance(user_id: int, amount: int):
    """Directly update balance for Battle results"""
    users_collection.update_one({"user_id": user_id}, {"$inc": {"balance": amount}})

# --- CORE COMMANDS ---
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target, error = await resolve_target(update, context)
    if not target: target = ensure_user_exists(update.effective_user)
    
    rank = users_collection.count_documents({"balance": {"$gt": target["balance"]}}) + 1
    msg = (
        f"👤 <b>User:</b> {get_mention(target)}\n"
        f"👛 <b>Balance:</b> <code>{format_money(target['balance'])}</code>\n"
        f"🏆 <b>Rank:</b> <code>#{rank}</code>"
    )
    await update.message.reply_text(msg, parse_mode=ParseMode.HTML)

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if users_collection.find_one({"user_id": user.id}): 
        return await update.message.reply_text("✨ Already registered!")
    
    ensure_user_exists(user)
    await update_balance(user.id, REGISTER_BONUS)
    await update.message.reply_text(f"🎉 Registered! Bonus: {format_money(REGISTER_BONUS)}")

async def claim(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat, user = update.effective_chat, update.effective_user
    if chat.type == ChatType.PRIVATE: return
    
    group_doc = groups_collection.find_one({"chat_id": chat.id})
    if group_doc and group_doc.get("claimed"): 
        return await update.message.reply_text("❌ Already claimed!")
    
    count = await context.bot.get_chat_member_count(chat.id)
    if count < MIN_CLAIM_MEMBERS:
        roast = await get_groq_response(f"Roast {user.first_name} for low members", user.first_name)
        return await update.message.reply_text(f"❌ Members: {count}/{MIN_CLAIM_MEMBERS}\n🔥 {stylize_text(roast)}")
    
    await update_balance(user.id, CLAIM_BONUS)
    groups_collection.update_one({"chat_id": chat.id}, {"$set": {"claimed": True}})
    await update.message.reply_text(f"💎 Claimed {format_money(CLAIM_BONUS)}!")
