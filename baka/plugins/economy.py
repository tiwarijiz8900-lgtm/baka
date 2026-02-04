# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Full Fix: Economy + AI + Battle Sync

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatType
from baka.config import REGISTER_BONUS, OWNER_ID, TAX_RATE, CLAIM_BONUS, MARRIED_TAX_RATE, SHOP_ITEMS, MIN_CLAIM_MEMBERS
from baka.utils import ensure_user_exists, get_mention, format_money, resolve_target, log_to_channel, stylize_text, track_group
from baka.database import users_collection, groups_collection
from baka.plugins.chatbot import get_groq_response 

# --- IMPORT ERROR FIXES ---

async def get_balance(user_id):
    """Used by battle and other plugins to check balance directly."""
    user = users_collection.find_one({"user_id": user_id})
    return user.get("balance", 0) if user else 0

async def update_balance(user_id, amount):
    """Used by battle and other plugins to update balance directly."""
    users_collection.update_one({"user_id": user_id}, {"$inc": {"balance": amount}})

# --- INVENTORY & CALLBACKS ---

async def inventory_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data.split("|")
    item_id = data[1]
    item = next((i for i in SHOP_ITEMS if i['id'] == item_id), None)
    if not item: 
        await query.answer("❌ Item data not found.", show_alert=True)
        return
    text = f"💎 Flex: {item['name']}\n💰 Value: {format_money(item['price'])}"
    await query.answer(text, show_alert=True)

# --- CORE COMMANDS ---

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user, chat = update.effective_user, update.effective_chat
    if chat.type != ChatType.PRIVATE:
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🚀 Register Here", url=f"https://t.me/{context.bot.username}?start=register")]])
        return await update.message.reply_text("❌ Register in PM first!", reply_markup=kb)

    if users_collection.find_one({"user_id": user.id}): 
        return await update.message.reply_text(f"✨ {get_mention(user)}, you are already registered!", parse_mode=ParseMode.HTML)
    
    ensure_user_exists(user)
    users_collection.update_one({"user_id": user.id}, {"$set": {"balance": REGISTER_BONUS}})
    await update.message.reply_text(f"🎉 Registered! Bonus: {format_money(REGISTER_BONUS)}", parse_mode=ParseMode.HTML)

async def claim(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat, user = update.effective_chat, update.effective_user
    if chat.type == ChatType.PRIVATE: return
    ensure_user_exists(user)
    track_group(chat, user)
    
    group_doc = groups_collection.find_one({"chat_id": chat.id})
    if group_doc and group_doc.get("claimed"): 
        return await update.message.reply_text("❌ Already claimed!")
    
    count = await context.bot.get_chat_member_count(chat.id)
    if count < MIN_CLAIM_MEMBERS:
        roast = await get_groq_response(f"Roast {user.first_name} for low members", user.first_name)
        return await update.message.reply_text(f"❌ Members: {count}/{MIN_CLAIM_MEMBERS}\n🔥 {stylize_text(roast)}", parse_mode=ParseMode.HTML)
    
    users_collection.update_one({"user_id": user.id}, {"$inc": {"balance": CLAIM_BONUS}})
    groups_collection.update_one({"chat_id": chat.id}, {"$set": {"claimed": True}})
    await update.message.reply_text(f"💎 Claimed {format_money(CLAIM_BONUS)}!", parse_mode=ParseMode.HTML)

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target, error = await resolve_target(update, context)
    if not target: target = ensure_user_exists(update.effective_user)
    rank = users_collection.count_documents({"balance": {"$gt": target["balance"]}}) + 1
    msg = f"👤 {get_mention(target)}\n👛 Balance: <code>{format_money(target['balance'])}</code>\n🏆 Rank: #{rank}"
    await update.message.reply_text(msg, parse_mode=ParseMode.HTML)

async def ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rich = users_collection.find().sort("balance", -1).limit(10)
    msg = "🏆 <b>RICH LEADERBOARD</b>\n\n"
    for i, d in enumerate(rich, 1): 
        msg += f"{i}. {get_mention(d)} » {format_money(d['balance'])}\n"
    await update.message.reply_text(msg, parse_mode=ParseMode.HTML)

async def give(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = ensure_user_exists(update.effective_user)
    args = context.args
    if not args: return await update.message.reply_text("Usage: `/give 100 @user`", parse_mode=ParseMode.HTML)
    # ... (Rest of give logic remains same)
