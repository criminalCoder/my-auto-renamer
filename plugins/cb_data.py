from helpo.utils import progress_for_pyrogram, convert
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helpo.database import db
import os
import humanize
from PIL import Image
import time
from config import *
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from plugins.lazydeveloper import verify_forward_status
from asyncio import Lock, Queue, create_task
import uuid
import hashlib

user_tasks = {}
user_locks = {}


@Client.on_callback_query(filters.regex('cancel'))
async def cancel(bot, update):
    try:
        await update.message.delete()
    except:
        return

@Client.on_callback_query(filters.regex('rename'))
async def rename(bot, update):
    user_id = update.message.chat.id
    date = update.message.date
    await update.message.delete()
    await update.message.reply_text("__𝙿𝚕𝚎𝚊𝚜𝚎 𝙴𝚗𝚝𝚎𝚛 𝙽𝚎𝚠 𝙵𝚒𝚕𝚎𝙽𝚊𝚖𝚎...__",
                                    reply_to_message_id=update.message.reply_to_message.id,
                                    reply_markup=ForceReply(True))

handler = {}

def manager(id, value):
    global handlers
    handler[id] = value
    return handler


def get_manager():
    global handler
    return handler

task_status_messages = {}  # {user_id: status_message_object}
task_details = {} 

# async def update_task_status_message(bot, user_id):
#     """Update the task status message for the user."""
#     if user_id not in user_tasks:
#         return  # No tasks to display for this user

#     # Get current task stats
#     active_count = user_tasks[user_id]["active"]
#     queue_count = user_tasks[user_id]["queue"].qsize()

#     # Build the status message
#     status_text = (
#         f"<blockquote>🛠 Task Status</blockquote>\n"
#         f"🚀 <b>Active Tasks</b>: <code>{active_count}</code>\n"
#         f"⏳ <b>In Queue</b>: <code>{queue_count}</code>\n"
#     )

#     # Check if a status message already exists
#     if user_id in task_status_messages:
#         try:
#             # Edit the existing message
#             await task_status_messages[user_id].edit_text(
#                 text=status_text,
#                 parse_mode=enums.ParseMode.HTML,
#             )
#         except Exception as e:
#             print(f"Failed to edit task status message: {e}")
#     else:
#         try:
#             # Send a new status message
#             status_message = await bot.send_message(
#                 chat_id=user_id,  # Send directly to the user
#                 text=status_text,
#                 parse_mode=enums.ParseMode.HTML,
#             )
#             task_status_messages[user_id] = status_message
#         except Exception as e:
#             print(f"Failed to send new task status message: {e}")

@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    user = message.from_user
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id)

    # Handle deep-linked arguments
    data = None
    if len(message.command) > 1:
        data = message.command[1]  # Extract the argument (e.g., task_id)

    # Default bot introduction message
    txt = (
        f"👋 Hey {user.mention}\n"
        "ɪ'ᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇ ғɪʟᴇ ʀᴇɴᴀᴍᴇʀ + ғɪʟᴇ ᴛᴏ ᴠɪᴅᴇᴏ ᴄᴏɴᴠᴇʀᴛᴇʀ ʙᴏᴛ ᴡɪᴛʜ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴛʜᴜᴍʙɴᴀɪʟ & ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ sᴜᴘᴘᴏʀᴛ!\n\n"
        "♥ ʙᴇʟᴏᴠᴇᴅ ᴏᴡɴᴇʀ <a href='https://telegram.me/Simplifytuber2'>ʏᴀsʜ ɢᴏʏᴀʟ</a> 🍟"
    )

    # Check if deep-linked data exists
    if data:
        # Handle specific deep-link actions (e.g., task details)
        if data.startswith("gettask_"):
            task_id = data.split("_", 1)[1]
            # Retrieve and display task details
            task = task_details.get(task_id)
            if task:
                details_txt = (
                    f"<b>Task Details</b>\n"
                    f"🆔 <b>Task ID</b>: <code>{task['id']}</code>\n"
                    f"📂 <b>Type</b>: {task['type']}\n"
                    f"📄 <b>New Name</b>: {task['new_name']}\n"
                    f"🔄 <b>Status</b>: {task['status']}\n"
                )
                await message.reply_text(details_txt, parse_mode=enums.ParseMode.HTML)
            else:
                await message.reply_text("❌ Task not found!", parse_mode=enums.ParseMode.HTML)
            return

    # Reply with the default bot introduction message
    button = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✿.｡:☆ ᴏᴡɴᴇʀ ⚔ ᴅᴇᴠs ☆:｡.✿", callback_data='dev')
        ],
        [
            InlineKeyboardButton('📢 ᴜᴘᴅᴀᴛᴇs §', url='https://t.me/botupdatesimplifytuber'),
            InlineKeyboardButton('🍂 sᴜᴘᴘᴏʀᴛ §', url='https://t.me/bysimplifytuber')
        ],
        [
            InlineKeyboardButton('🍃 ᴀʙᴏᴜᴛ §', callback_data='about'),
            InlineKeyboardButton('ℹ ʜᴇʟᴘ §', callback_data='help')
        ]
    ])

    if START_PIC:
        await message.reply_photo(START_PIC, caption=txt, reply_markup=button)
    else:
        await message.reply_text(text=txt, reply_markup=button, disable_web_page_preview=True)


@Client.on_message(filters.private & filters.command("gettask"))
async def get_task_details(bot, message):
    """Handle /gettask command."""
    try:
        user_id = message.from_user.id
        if len(message.command) < 2:
            await message.reply("❗ Usage: /gettask <task_id>")
            return

        task_id = message.command[1]
        if task_id not in task_details:
            await message.reply(f"❌ Task with ID <code>{task_id}</code> not found!", parse_mode=enums.ParseMode.HTML)
            return

        task_data = task_details[task_id]
        status_text = (
            f"<blockquote>🤞 Task Details ⏳< blockquote>\n"
            f"🆔 <b>Task ID</b>: <code>{task_data['id']}</code>\n"
            f"📂 <b>Type</b>: {task_data['type']}\n"
            f"📄 <b>New Name</b>: {task_data['new_name']}\n"
            f"🔄 <b>Status</b>: {task_data['status']}\n"
        )
        await message.reply(status_text, parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        print(f"Error in get_task_details: {e}")

# async def update_task_status_message(bot, user_id):
#     """Send a new status message and delete the old one."""
#     if user_id not in user_tasks:
#         return  # No tasks for this user

#     # Fetch current task stats
#     active_count = user_tasks[user_id]["active"]
#     queue_count = user_tasks[user_id]["queue"].qsize()

#     # Build the status message
#     status_text = (
#         f"<blockquote>🛠 Task Status</blockquote>\n"
#         f"🚀 <b>Active Tasks</b>: <code>{active_count}</code>\n"
#         f"⏳ <b>In Queue</b>: <code>{queue_count}</code>\n"
#     )

#     # Send the new status message
#     try:
#         # Delete the previous status message if it exists
#         if user_id in task_status_messages:
#             try:
#                 await task_status_messages[user_id].delete()
#             except Exception as e:
#                 print(f"Failed to delete previous status message: {e}")

#         # Send a new status message and save its reference
#         new_status_message = await bot.send_message(
#             chat_id=user_id,
#             text=status_text,
#             parse_mode=enums.ParseMode.HTML,
#         )
#         task_status_messages[user_id] = new_status_message
#     except Exception as e:
#         print(f"Failed to send new task status message: {e}")

async def generate_short_task_id():
    """Generate a hash-based unique short task ID."""
    full_uuid = str(uuid.uuid4())
    hash_object = hashlib.md5(full_uuid.encode())  # Use MD5 hashing
    return hash_object.hexdigest()[:8]

async def update_task_status_message(bot, user_id):
    """Send a detailed status message and delete the old one."""
    if user_id not in user_tasks:
        return  # No tasks for this user

    # Fetch current task stats
    active_count = user_tasks[user_id]["active"]
    queue = list(user_tasks[user_id]["queue"]._queue)  # Extract queued tasks
    queue_count = len(queue)

    # Build the detailed status message
    status_text = "<blockquote><b>🥂🍟⏳ ᴛʜᴇ ᴛᴀꜱᴋ ᴍᴀɴᴀɢᴇʀ ⏳🍟🥂</b></blockquote>\n"
    status_text += "╭━━❰❤.<b>ʟᴀᴢʏᴅᴇᴠᴇʟᴏᴘᴇʀ</b>.❤❱━━➣\n"
    await asyncio.sleep(2)
    for index, task in enumerate(queue, start=1):
        task_id = task["id"]
        await asyncio.sleep(2)
        status_text += (
            f"┣⪼🍿 <b>ᴛᴀꜱᴋ {index}</b> ➣ <code>{task_id}</code>\n"
            f"┣⪼⚙ <b><a href='https://t.me/{bot.username}?start=gettask_{task_id}'>ɢᴇᴛ ᴅᴇᴛᴀɪʟꜱ : ᴄʟɪᴄᴋ ʜᴇʀᴇ</a></b>\n"
            f"┣━━━━━━━━━━━━━━━━━━━ \n"
        )

    # Add summary of active and queued tasks
    await asyncio.sleep(1)
    status_text += (
        f"┣📜 <b>ᴀᴄᴛɪᴠᴇ ᴛᴀꜱᴋꜱ</b>: <code>{active_count}</code> | ⏳<b>ɪɴ ϙᴜᴇᴜᴇ</b>: <code>{queue_count}</code>\n"
        "╰━━━━━━━━━━━━━━━━━━━➣"
    )

    # Delete the previous status message if it exists
    await asyncio.sleep(1)
    if user_id in task_status_messages:
        try:
            await task_status_messages[user_id].delete()
        except Exception as e:
            print(f"Failed to delete previous status message: {e}")

    # Send a new detailed status message and save its reference
    await asyncio.sleep(1)
    try:
        new_status_message = await bot.send_message(
            chat_id=user_id,
            text=f"{status_text}\n\n🍟" ,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True,
        )
        task_status_messages[user_id] = new_status_message
    except Exception as e:
        print(f"Failed to send new task status message: {e}")

# @Client.on_callback_query(filters.regex("upload"))
async def lazydevelopertaskmanager(bot, message, new_file_name, lazymsg):
    try:
        user_id = message.from_user.id
        await lazymsg.edit("<b>ɪɴɪᴛɪᴀᴛɪɴɢ ᴛᴀsᴋ....<b>")
        # Initialize user-specific task tracking if not present
        if user_id not in user_tasks:
            user_tasks[user_id] = {
                "active": 0,  # Active renaming tasks
                "queue": Queue(),  # Pending tasks queue
            }
            user_locks[user_id] = Lock()  # Lock for managing task execution
        
        task_id = await generate_short_task_id()
        
        task_data = {
            "id":task_id,
            "update": message,
            "type": "video",
            "new_name": new_file_name,
            "status": "Pending",
        }
        task_details[task_id] = task_data 
        # Manage task execution
        async with user_locks[user_id]:
            if user_tasks[user_id]["active"] >= MAX_ACTIVE_TASKS:
                # Add task to queue
                await user_tasks[user_id]["queue"].put(task_data)
                task_data["status"] = "Queued"
                # sweetreply = await lazymsg.edit("<b>🔄 ᴛᴀsᴋ ɪs ɪɴ ᴛʜᴇ qᴜᴇᴜᴇ. ɪᴛ ᴡɪʟʟ sᴛᴀʀᴛ sᴏᴏɴ. ⏳</b>")
            else:
                # Increment active tasks and process immediately
                user_tasks[user_id]["active"] += 1
                task_data["status"] = "Processing"
                create_task(process_task(bot, user_id, task_data, lazymsg))  # Start task in background
        
        await update_task_status_message(bot, user_id)
        # await sweetreply.delete()
    except Exception as e:
        print(f"Error in lazydevelopertaskmanager: {e}")

async def process_task(bot, user_id, task_data, lazymsg):
    try:
        update = task_data["update"]
        new_name = task_data["new_name"]
        task_id = task_data["id"]
        task_details[task_id]["status"] = "Processing"
        # print(f"task for user id {update.from_user.id}")
        manager(user_id, True)
        type = task_data["type"]
        new_filename = new_name
        file_path = f"downloads/{user_id}{time.time()}/{new_filename}"
        await lazymsg.edit("<b>⏳ ᴘʀᴇᴘᴀʀɪɴɢ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ...</b>")
        c_time = time.time()
         # Check if the message contains media (Video or Document)
        if not (update.video or update.document):
            print("No media found to preocess...")
            # return await update.reply("No media file found to process.")
        try:
            path = await update.download(file_name=file_path, progress=progress_for_pyrogram, progress_args=(f"🔥 ᴅᴏᴡɴʟᴏᴀᴅ ɪɴ ᴘʀᴏɢʀᴇss...\n<blockquote>{new_filename}</blockquote>", lazymsg, c_time))
            # print(f"download completed |=> 🤞")
        except Exception as e:
            return await lazymsg.edit(e)
        duration = 0
        try:
            # print(f" Trying to get duration |=> {duration}")
            metadata = extractMetadata(createParser(file_path))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            # print(f"Got duration ✅|=> {duration}")
        except:
            pass
        ph_path = None
        # print(f"Trying to get media |=> ")
        media = getattr(update, update.media.value)
        # print(f" Got media |=> {media} ")
        # media = file
        c_caption = await db.get_caption(update.chat.id)
        c_thumb = await db.get_thumbnail(update.chat.id)
        if c_caption:
            try:
                caption = c_caption.format(filename=new_filename, filesize=humanize.naturalsize(media.file_size),
                                        duration=convert(duration))
            except Exception as e:
                await lazymsg.edit(text=f"Your caption Error unexpected keyword ●> ({e})")
                return
        else:
            caption = f"{new_filename}"
        # print(f"Trying to get thumbnail")
        if (media.thumbs or c_thumb):
            if c_thumb:
                ph_path = await bot.download_media(c_thumb)
            else:
                ph_path = await bot.download_media(media.thumbs[0].file_id)
            Image.open(ph_path).convert("RGB").save(ph_path)
            img = Image.open(ph_path)
            img.resize((320, 320))
            img.save(ph_path, "JPEG")
        # print(f"🤳 Got Thumbnail |=> ✅")
        await lazymsg.edit("<b>⚡ ᴘʀᴇᴘᴀʀɪɴɢ ᴛᴏ ᴜᴘʟᴏᴀᴅ...</b>")
        c_time = time.time()
        try:
            # Attempt to retrieve the forward ID and target chat ID from the database
            forward_id = await db.get_forward(update.from_user.id)
            lazy_target_chat_id = await db.get_lazy_target_chat_id(update.from_user.id)
            
            # Check if either of them is `None` or invalid
            if not forward_id or not lazy_target_chat_id:
                await bot.send_message(
                    chat_id=update.chat.id,
                    text="sᴏʀʀʏ sᴡᴇᴇᴛʜᴇᴀʀᴛ, ɪ'ᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴠᴇʀsɪᴏɴ ᴏꜰ ᴛʜᴇ ʀᴇɴᴀᴍᴇʀ ʙᴏᴛ.\n❌ ꜰᴏʀᴡᴀʀᴅ ɪᴅ ᴏʀ ᴛᴀʀɢᴇᴛ ᴄʜᴀᴛ ɪᴅ ɴᴏᴛ sᴇᴛ. ᴘʟᴇᴀsᴇ ᴄᴏɴꜰɪɢᴜʀᴇ ᴛʜᴇᴍ ꜰɪʀsᴛ. 💔"
                )
                return  # Stop further execution
        except Exception as e:
            print(f"Error retrieving IDs: {e}")
            await bot.send_message(
                chat_id=update.chat.id,
                text="❌ ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ʀᴇᴛʀɪᴇᴠɪɴɢ ᴛʜᴇ ᴄᴏɴꜰɪɢᴜʀᴀᴛɪᴏɴ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ."
            )
            return  # Stop further execution

        try:
            if type == "document":
                suc = await bot.send_document(
                    update.chat.id,
                    document=file_path,
                    thumb=ph_path,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=(f"<b>==========x==========</b>⏳ ᴜᴘʟᴏᴀᴅ ɪɴ ᴘʀᴏɢʀᴇss... 🚀\n<b>==========x==========</b>\n<blockquote>{new_filename}</blockquote>", lazymsg, c_time),
                    parse_mode=enums.ParseMode.HTML
                )
            elif type == "video":
                suc = await bot.send_video(
                    update.chat.id,
                    video=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("⏳ ᴜᴘʟᴏᴀᴅ ɪɴ ᴘʀᴏɢʀᴇss... 🚀\n<blockquote>{new_filename}</blockquote>", lazymsg, c_time)
                )
            elif type == "audio":
                suc = await bot.send_audio(
                    update.chat.id,
                    audio=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("⏳ ᴜᴘʟᴏᴀᴅ ɪɴ ᴘʀᴏɢʀᴇss... 🚀", lazymsg, c_time)
                )
            try:
                # await lazymsg.edit(f"<b>❤--sᴍɪʟᴇ-ᴘʟᴇᴀsᴇ--❤<b>")
                await lazymsg.delete()
                await asyncio.sleep(1)
                sent = await suc.copy(forward_id)
                # await suc.copy(lazy_target_chat_id)
                if sent:
                    # finally delete the renamed file
                    await suc.delete()
            except Exception as e:
                pass
        except Exception as e:
            await lazymsg.edit(f" Erro {e}")
            print(f"Error => {e}")
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)

        if not await verify_forward_status(user_id):
            return await bot.send_message(user_id, f"Stop forward triggered, Happy renaming 🤞")

        try:
            print("-----🍟. LazyDeveloperr .🍟-----")
            sessionstring = await db.get_session(user_id)
            apiid = await db.get_api(user_id)
            apihash = await db.get_hash(user_id)
            # Check if any value is missing
            if not sessionstring or not apiid or not apihash:
                missing_values = []
                if not sessionstring:
                    missing_values.append("SESSION STRING")
                if not apiid:
                    missing_values.append("API ID")
                if not apihash:
                    missing_values.append("API hash")
                
                missing_fields = ", ".join(missing_values)
                await bot.send_message(
                    chat_id=update.chat.id,
                    text=f"⛔ ᴍɪssɪɴɢ ʀᴇQᴜɪʀᴇᴅ ɪɴғᴏʀᴍᴀᴛɪᴏɴ:<b> {missing_fields}. </b>\n\nᴘʟᴇᴀsᴇ ᴇɴsᴜʀᴇ ʏᴏᴜ ʜᴀᴠᴇ sᴇᴛ ᴜᴘ ᴀʟʟ ᴛʜᴇ ʀᴇQᴜɪʀᴇᴅ ᴅᴇᴛᴀɪʟs ɪɴ ᴛʜᴇ ᴅᴀᴛᴀʙᴀsᴇ.",
                    parse_mode=enums.ParseMode.HTML
                )
                return  # Exit the function if values are missing
            
            run_lazybot = TelegramClient(StringSession(sessionstring), apiid, apihash)
            await run_lazybot.start()
            print("🔥 user bot initiated 🚀 ")

            # (C) LazyDeveloperr ❤
            forwarded_lazy_count = 0
            max_forward_lazy_count = 1
            skiped_lazy_files = 0
            # (C) LazyDeveloperr ❤
            try:
                async for msg in run_lazybot.iter_messages(lazy_target_chat_id, limit=10):
                    # Forward or process the message
                    if forwarded_lazy_count >= max_forward_lazy_count:
                        forwarded_lazy_count = 0
                        break
                    got_lazy_file = msg.document or msg.video or msg.audio

                    if got_lazy_file:  # Check if the message contains media
                        filesize = msg.document.size if msg.document else msg.video.size if msg.video else msg.audio.size if msg.audio else 0
                        lazydeveloper_size = 2090000000
                        if filesize < lazydeveloper_size:
                            # await lgbtq.forward_messages('@LazyDevDemo_BOT', msg.id, target_chat_id)
                            await run_lazybot.send_message(BOT_USERNAME, msg.text or "", file=got_lazy_file)
                            # print(f"✅ Forwarded media with ID {msg.id}")
                            await asyncio.sleep(1)
                            await run_lazybot.delete_messages(lazy_target_chat_id, msg.id)
                            forwarded_lazy_count += 1
                        else:
                            await bot.send_message(
                                update.from_user.id,
                                f"👠 sᴋɪᴘᴘᴇᴅ ᴍᴇᴅɪᴀ ᴡɪᴛʜ ɪᴅ {msg.id}, sɪᴢᴇ ɢʀᴇᴀᴛᴇʀ ᴛʜᴀɴ 2ɢʙ"
                                )
                            # skiped_lazy_files += 1
                            print(f"👠 Skipped media with ID {msg.id}, Size greater than 2gb")
                            await asyncio.sleep(1)

                    else:
                        print(f"Skipped non-media message with ID {msg.id}")


            except Exception as e:
                print(f"Error occurred: {e}")
                return await update.reply("❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ᴍᴇssᴀɢᴇs 💔")

            # 
            # 
            # (C) LazyDeveloperr ❤
            print(f"❤ New file forwarded to bot after renaming 🍟")
            await run_lazybot.disconnect()
            if not run_lazybot.is_connected():
                print("Session is disconnected successfully!")
            else:
                print("Session is still connected.")
            print("-----🍟. LazyDeveloperr .🍟----- ")

            # (C) LazyDeveloperr ❤
            # 
            #
            #
            
        except Exception as e:
            print(f"Error deleting original file message =/= lastt message -> Check code in cb_data fom line no 257 to 306 @LazyDeveloperr ❤\n: {e}")
        
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)

    except Exception as lazydeveloperr:
        print(lazydeveloperr)
        task_details[task_id]["status"] = "Failed"
    finally:
        print(f"Finally block is being called")
        # Decrement active task count and process next task from queue
        try:
            async with user_locks[user_id]:
                user_tasks[user_id]["active"] -= 1
                if not user_tasks[user_id]["queue"].empty():
                    next_task = await user_tasks[user_id]["queue"].get()
                    smss = await bot.send_message(user_id, text=f"<b>🤞 ɪɴɪᴛɪᴀᴛɪɴɢ ɴᴇxᴛ ϙᴜᴇᴜᴇᴅ ᴛᴀꜱᴋ...<b>", parse_mode=enums.ParseMode.HTML)
                    user_tasks[user_id]["active"] += 1
                    next_task["status"] = "Processing"
                    await trigger_next_task(bot, user_id, next_task, smss)
            # Update the task status message
            await update_task_status_message(bot, user_id)
        except Exception as e:
            print(f"Error occ => {e}")

async def trigger_next_task(bot, user_id, next_task, smss):
    create_task(process_task(bot, user_id, next_task, smss))  # Start next task in background
