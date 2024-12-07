
class mr(object):
    PROGRESS_BAR = """\n
╭━━━━❰❤.ʏᴀsʜ ɢᴏʏᴀʟ.❤❱━➣
┣⪼ 🗂️ : {1} | {2}
┣⪼ ⏳️ : {0}%
┣⪼ 🚀 : {3}/s
┣⪼ ⏱️ : {4}
╰━━━━━━━━━━━━━━━➣ """

    ABOUT_TXT = """
╭───────────⍟
├🤖 ᴍʏ ɴᴀᴍᴇ : {}
├👑 ᴏᴡɴᴇʀ : <a href=https://t.me/Simplifytuber2>Yash Goyal</a> 
├🦋 ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href=https://telegram.me/LazyDeveloperr>LazyDeveloperr</a> 
├👨‍💻 ᴘʀᴏɢʀᴀᴍᴇʀ : <a href=https://github.com/LazyDeveloperr>LazyDeveloperr</a>
├📕 ʟɪʙʀᴀʀʏ : <a href=https://github.com/pyrogram>ᴘʏʀᴏɢʀᴀᴍ</a>
├✏️ ʟᴀɴɢᴜᴀɢᴇ : <a href=https://www.python.org>ᴘʏᴛʜᴏɴ 3</a>
├💾 ᴅᴀᴛᴀ ʙᴀsᴇ : <a href=https://cloud.mongodb.com>ᴍᴏɴɢᴏᴅʙ</a>
├📊 ʙᴜɪʟᴅ sᴛᴀᴜs : v2.1.90 [ ꜱɪɢᴍᴀ 🗿 ]
╰───────────────⍟

"""
    HELP_TXT = """
🍿 <b><u>ʜᴏᴡ ᴛᴏ sᴛᴀʀᴛ ʀᴇɴᴀᴍᴇ ᴘʀᴏᴄᴇss</u></b>
•> /generate ᴜsᴇ ᴛʜɪs cmd ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴛᴇʟᴇᴛʜᴏɴ sᴇssɪᴏɴ sᴛʀɪɴɢ. ɪғ ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ ʜᴀᴠᴇ ᴛᴇʟᴇᴛʜᴏɴ sᴇssɪᴏɴ, ᴜsᴇ /ᴄᴏɴɴᴇᴄᴛ
•> /connect ᴜsᴇ ᴛʜɪs cmd ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ʏᴏᴜʀ sᴇssɪᴏɴ(ᴛᴇʟᴇᴛʜᴏɴ)
•> /rename ᴜsᴇ ᴛʜɪs cmd ɪғ ʏᴏᴜ ʜᴀᴠᴇ ʟᴏɢɢᴇᴅ ɪɴ sᴜᴄᴄᴇssғᴜʟʟʏ ᴀɴᴅ ғᴏʟʟᴏᴡ ɪɴsᴛʀᴜᴄᴛɪᴏɴs.

📸 <b><u>ʜᴏᴡ ᴛᴏ sᴇᴛ ᴛʜᴜᴍʙɴɪʟᴇ</u></b>
•> /start ᴀ ʙᴏᴛ ᴀɴᴅ sᴇɴᴅ ᴀɴʏ ᴘɪᴄᴛᴜʀᴇ ᴛᴏ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ sᴇᴛ ᴛʜᴜᴍʙɴɪʟᴇ.
•> /delthumb ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴀɴᴅ ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴏʟᴅ ᴛʜᴜᴍʙɴɪʟᴇ.
•> /viewthumb ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ vɪᴇᴡ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ᴛʜᴜᴍʙɴɪʟᴇ.

📑 <b><u>ʜᴏᴡ ᴛᴏ sᴇᴛ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ</u></b>
•> /set_caption - sᴇᴛ ᴀ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ
•> /see_caption - sᴇᴇ ʏᴏᴜʀ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ
•> /del_caption - ᴅᴇʟᴇᴛᴇ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ

ᴇxᴀᴍᴘʟᴇ:- /set_caption 📕 ғɪʟᴇ nᴀᴍᴇ: {filename}
💾 sɪᴢᴇ: {filesize}
⏰ dᴜʀᴀᴛɪᴏɴ: {duration}


🆘𝗰𝗼𝗻𝘁𝗮𝗰𝘁 :- <a href=https://t.me/Simplifytuber2>ʏᴀsʜ ɢᴏʏᴀʟ</a> - ғᴏʀ ᴀɴʏ ʜᴇʟᴘ 🆘
"""

#⚠️ don't remove our credits 🙏😢😢
    DEV_TXT = """
<b>ᴏᴡɴᴇʀ & ᴅᴇᴠᴇʟᴏᴘᴇʀs</b>

• ᴏᴡɴᴇʀ : <a href=https://t.me/Simplifytuber2>👑 ʏᴀsʜ ɢᴏʏᴀʟ👑</a>  
• ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href=https://t.me/LazyDeveloperr>🍟LazyDeveloperr❤</a>

"""
