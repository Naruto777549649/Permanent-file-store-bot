import os
import pymongo
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🔥 Environment Variables
API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")
MONGO_URL = os.getenv("MONGO_URL", "your_mongodb_url")
ADMIN_ID = int(os.getenv("ADMIN_ID", "7019600964"))  # Change Admin ID

# 🔗 MongoDB Connection
mongo_client = pymongo.MongoClient(MONGO_URL)
db = mongo_client["FileStore"]
collection = db["files"]

# 🤖 Initialize Bot
bot = Client("FileStoreBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# 📌 Start Command
@bot.on_message(filters.command("start"))
async def start(client, message):
    user_name = message.from_user.first_name
    buttons = [
        [InlineKeyboardButton("HELP", callback_data="help"), InlineKeyboardButton("ABOUT", callback_data="about")],
        [InlineKeyboardButton("CREATE MY OWN CLONE", url="https://github.com/your_repo")],
        [InlineKeyboardButton("📢 UPDATE CHANNEL", url="https://t.me/Dragon_ball_7521")]
    ]
    await message.reply_text(
        f"Hello 𝙂𝙤𝙙 {user_name} ✨\n\n"
        "I am a permanent file store bot. You can store messages/files and access them via shareable links.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# 📂 Generate Link Command
@bot.on_message(filters.command("genlink") & filters.reply)
async def gen_link(client, message):
    file_id = message.reply_to_message.message_id
    file_info = {
        "file_id": file_id,
        "user_id": message.from_user.id
    }
    collection.insert_one(file_info)
    file_link = f"https://t.me/{client.me.username}?start=file_{file_id}"
    await message.reply_text(f"✅ File stored successfully!\n🔗 Link: {file_link}")


# 📤 Retrieve Stored File
@bot.on_message(filters.regex(r"^/start file_(\d+)"))
async def send_file(client, message):
    file_id = int(message.matches[0].group(1))
    file_info = collection.find_one({"file_id": file_id})
    if file_info:
        await client.forward_messages(message.chat.id, from_chat_id=message.chat.id, message_ids=file_id)
    else:
        await message.reply_text("❌ File not found!")


# 🔗 Shorten Any Link
@bot.on_message(filters.command("shortener"))
async def shortener(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Please provide a valid link.")
    original_link = message.command[1]
    short_link = f"https://t.me/{client.me.username}?start=short_{original_link}"
    await message.reply_text(f"🔗 Shortened Link: {short_link}")


# 🚀 Run the Bot
bot.run()
