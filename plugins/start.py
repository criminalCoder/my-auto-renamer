from asyncio import sleep
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery, Message
from pyrogram.errors import FloodWait
import humanize
import random
from helpo.txt import mr
from helpo.database import db
from config import START_PIC, FLOOD, ADMIN 



# ===========================================================================
# ===========================================================================
                    ### AUTO RENAME = STEP 1
# ===========================================================================

import re
import requests

TMDB_API_KEY = "3c3c555373fb569efa022af1ed58f4c8"

def extract_movie_name(filename):
    """
    Extracts a clean movie name and year from the filename.
    """
    # Try to extract "Movie Name (Year)"
    match = re.search(r"([a-zA-Z\s]+)\((\d{4})\)", filename)
    if match:
        return match.group(1).strip() + " (" + match.group(2) + ")"
    
    # Clean up filename if no exact match
    filename = re.sub(r"[\[\]\(\)\-_\.\@\d+pHEVC|HDRip|AAC|x\d+|Subs|Series|Movies|Hindi|English|x\d+|BluRay|WEB|MKV|MP4]", " ", filename, flags=re.IGNORECASE)
    filename = re.sub(r"\s+", " ", filename).strip()
    return filename

def search_tmdb(movie_name):
    """
    Searches TMDb for the given movie name and returns the top result.
    """
    url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_name,
        "include_adult": False,
    }
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return f"Error: Unable to reach TMDb (status code: {response.status_code})"
    
    data = response.json()
    if data.get("results"):
        top_result = data["results"][0]
        title = top_result.get("title", "Unknown Title")
        release_date = top_result.get("release_date", "Unknown Date")
        year = release_date.split("-")[0] if release_date else "Unknown Year"
        return f"{title} ({year})"
    
    return "Movie not found on TMDb."

@Client.on_message(filters.private & filters.document)
async def handle_file(client, message: Message):
    """
    Handles file uploads in private chat. Extracts the movie name and searches TMDb.
    """
    file_name = message.document.file_name
    movie_name = extract_movie_name(file_name)
    
    await message.reply_text(f"Searching TMDb for: {movie_name}...")
    
    tmdb_title = search_tmdb(movie_name)
    await message.reply_text(f"Original Title from TMDb: {tmdb_title}")




# ===========================================================================
                    ### ./ AUTO RENAME = STEP 1
# ===========================================================================
# ===========================================================================




@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    user = message.from_user
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id)             
    txt=f"👋 Hey {user.mention} \nɪ'ᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇ ғɪʟᴇ ʀᴇɴᴀᴍᴇʀ + ғɪʟᴇ ᴛᴏ ᴠɪᴅᴇᴏ ᴄᴏɴᴠᴇʀᴛᴇʀ ʙᴏᴛ ᴡɪᴛʜ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴛʜᴜᴍʙɴᴀɪʟ & ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ sᴜᴘᴘᴏʀᴛ!\n\n♥ ʙᴇʟᴏᴠᴇᴅ ᴏᴡɴᴇʀ <a href='https://telegram.me/Simplifytuber2'>ʏᴀsʜ ɢᴏʏᴀʟ</a> 🍟"
    button=InlineKeyboardMarkup([[
        InlineKeyboardButton("✿.｡:☆ ᴏᴡɴᴇʀ ⚔ ᴅᴇᴠs ☆:｡.✿", callback_data='dev')
        ],[
        InlineKeyboardButton('📢 ᴜᴘᴅᴀᴛᴇs §', url='https://t.me/botupdatesimplifytuber'),
        InlineKeyboardButton('🍂 sᴜᴘᴘᴏʀᴛ §', url='https://t.me/bysimplifytuber')
        ],[
        InlineKeyboardButton('🍃 ᴀʙᴏᴜᴛ §', callback_data='about'),
        InlineKeyboardButton('ℹ ʜᴇʟᴘ §', callback_data='help')
        ]])
    if START_PIC:
        await message.reply_photo(START_PIC, caption=txt, reply_markup=button)       
    else:
        await message.reply_text(text=txt, reply_markup=button, disable_web_page_preview=True)


# @Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
# async def rename_start(client, message):
#     file = getattr(message, message.media.value)
#     filename = file.file_name
#     filesize = humanize.naturalsize(file.file_size) 
#     fileid = file.file_id
#     try:
#         text = f"""**__What do you want me to do with this file.?__**\n\n**File Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""
#         buttons = [[ InlineKeyboardButton("📝 𝚂𝚃𝙰𝚁𝚃 𝚁𝙴𝙽𝙰𝙼𝙴 📝", callback_data="rename") ],
#                    [ InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="cancel") ]]
#         await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
#         await sleep(FLOOD)
#     except FloodWait as e:
#         await sleep(e.value)
#         text = f"""**__What do you want me to do with this file.?__**\n\n**File Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""
#         buttons = [[ InlineKeyboardButton("📝 𝚂𝚃𝙰𝚁𝚃 𝚁𝙴𝙽𝙰𝙼𝙴 📝", callback_data="rename") ],
#                    [ InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="cancel") ]]
#         await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
#     except:
#         pass

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    if data == "start":
        await query.message.edit_text(
            text=f"""👋 Hey {query.from_user.mention} \nɪ'ᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇ ғɪʟᴇ ʀᴇɴᴀᴍᴇʀ + ғɪʟᴇ ᴛᴏ ᴠɪᴅᴇᴏ ᴄᴏɴᴠᴇʀᴛᴇʀ ʙᴏᴛ ᴡɪᴛʜ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴛʜᴜᴍʙɴᴀɪʟ & ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ sᴜᴘᴘᴏʀᴛ!\n\n♥ ʙᴇʟᴏᴠᴇᴅ ᴏᴡɴᴇʀ <a href='https://telegram.me/Simplifytuber2'>ʏᴀsʜ ɢᴏʏᴀʟ</a> 🍟""",
            reply_markup=InlineKeyboardMarkup( [[
                InlineKeyboardButton("✿.｡:☆ ᴏᴡɴᴇʀ ⚔ ᴅᴇᴠs ☆:｡.✿", callback_data='dev')
                ],[
                InlineKeyboardButton('📢 ᴜᴘᴅᴀᴛᴇs §', url='https://t.me/botupdatesimplifytuber'),
                InlineKeyboardButton('🍂 sᴜᴘᴘᴏʀᴛ §', url='https://t.me/bysimplifytuber')
                ],[
                InlineKeyboardButton('🍃 ᴀʙᴏᴜᴛ §', callback_data='about'),
                InlineKeyboardButton('ℹ ʜᴇʟᴘ §', callback_data='help')
                ]]
                )
            )
    elif data == "help":
        await query.message.edit_text(
            text=mr.HELP_TXT,
            reply_markup=InlineKeyboardMarkup( [[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    elif data == "about":
        await query.message.edit_text(
            text=mr.ABOUT_TXT.format(client.mention),
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup( [[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    elif data == "dev":
        await query.message.edit_text(
            text=mr.DEV_TXT,
            reply_markup=InlineKeyboardMarkup( [[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            await query.message.delete()





