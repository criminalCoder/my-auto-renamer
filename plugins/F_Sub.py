from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helpo.utils import not_subscribed
from config import FORCE_SUB

@Client.on_message(filters.private & filters.create(not_subscribed))
async def is_not_subscribed(client, message):
    buttons = [[ InlineKeyboardButton(text="📢𝙹𝚘𝚒𝚗 𝚄𝚙𝚍𝚊𝚝𝚎 𝙲𝚑𝚊𝚗𝚗𝚎𝚕📢", url=f"https://t.me/{FORCE_SUB}") ]]
    text = "**Please Join our Updates Channel to use this bot**"
    await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
