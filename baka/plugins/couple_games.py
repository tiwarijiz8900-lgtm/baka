import random
from telegram import Update
from telegram.ext import ContextTypes

# ======================================================
# 🔥 UNLIMITED DATA (Inhe aap jitna chahe bada sakte hain)
# ======================================================

TRUTHS = [
    "Kya tumne kabhi kisi se flirt karne ke liye jhoot bola hai? 😉",
    "Tumhari sabse badi insecurity kya hai? 🙈",
    "Kya tum abhi bhi apne ex ke baare mein sochte ho? 🤫",
    "Tumne kabhi kisi ko galat message bhej kar delete kiya hai? 😂",
    "Agar tumhe mujhse ek sach chhupana ho, toh wo kya hoga? 😇",
    "Kya tumne kabhi kisi ki profile stalk ki hai? 📱",
    "Tumhe mujh mein sabse buri aadat kya lagti hai? 🙊",
    "Pehli nazar ka pyaar ya pehli nazar ka dhoka? 💘",
    "Tumne kabhi kisi ke saath screen sharing mein galti ki hai? 🖥️",
    "Tumhara sabse bada 'guilty pleasure' kya hai? 🍫"
]

DARES = [
    "Apne partner ko 'I Love You' bolo voice note mein! 🎙️",
    "Apne phone ka last screenshot group mein bhejo! 📸",
    "Kisi ko bhi randomly 'I miss you' message karo aur screenshot dikhao! 🔥",
    "Agli 2 minute tak sirf emoji mein baat karo 😶",
    "Apne bio mein likho 'Angel's Property' 😇",
    "Group mein ek romantic gaana gao! 🎵",
    "Apne crush ka naam bina sharmaye batao! 😍",
    "Ek selfie bhejo abhi bina filter ke! 🤳",
    "Apne status pe likho 'Main Pagal Hoon' aur 5 min rehne do! 🤪"
]

QUIZZES = [
    {"q": "Sacha pyaar kitni baar hota hai?", "a": "Sirf ek baar... ya shayad har baar? 😉"},
    {"q": "Relationship mein trust zyada bada hai ya respect?", "a": "Dono hi barabar hain! ❤️"},
    {"q": "Ek perfect date kahan honi chahiye?", "a": "Coffee, Dinner ya Long drive? 🕯️"},
    {"q": "Kya break-up ke baad dosti ho sakti hai?", "a": "Ye toh dil pe depend karta hai! 💔"},
    {"q": "Ladkiyon ko sabse zyada kya pasand hai?", "a": "Care, Time aur Attention! ✨"}
]

# ======================================================
# 🎮 LOGIC: JO HAR BAAR CHANGE HOTA RAHE
# ======================================================

async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # random.sample use karne se repetition kam hoti hai
    question = random.choice(TRUTHS)
    name = update.effective_user.first_name
    await update.message.reply_text(f"✨ **TRUTH FOR {name}** ✨\n\n{question}\n\nJhoot mat bolna, Angel sab dekh rahi hai! 😉")

async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task = random.choice(DARES)
    name = update.effective_user.first_name
    await update.message.reply_text(f"🔥 **DARE FOR {name}** 🔥\n\n{task}\n\nPure nahi kiya toh Angel naraz ho jayegi! 😘")

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item = random.choice(QUIZZES)
    await update.message.reply_text(f"🧠 **LOVE QUIZ** 🧠\n\nSawal: {item['q']}\n\nAngel tumhara jawab sunna chahti hai! ❤️")
