import os
import re
from platform import python_version as ramdi
from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from EmikoRobot.events import register
from EmikoRobot import telethn as tbot

PHOTO = "https://telegra.ph/file/7b5477ae0c4771a524d74.jpg"
@register(pattern=("/alive"))
async def awake(event):
  TEXT = f"**ʜɪɪ [{event.sender.first_name}](tg://user?id={event.sender.id}),『 ɪ'ᴍ ᴄᴜᴛɪᴇᴘɪᴇ 』** \n\n"
  TEXT += "✰**I'ᴍ ᴡᴏʀᴋɪɴɢ ᴩʀᴏᴩᴇʀʟy** \n\n"
  TEXT += f"✰ **My ᴍᴀꜱᴛᴇʀ : [ᴀɴᴏɴ](https://t.me/itzmeanon)** \n\n"
  TEXT += f"✰ **Lɪʙʀᴀʀy ᴠᴇʀꜱɪᴏɴ :** `{telever}` \n\n"
  TEXT += f"✰**Tᴇʟᴇᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ :** `{tlhver}` \n\n"
  TEXT += f"✰ **Pyʀᴏɢʀᴀᴍ ᴠᴇʀꜱɪᴏɴ :** `{pyrover}` \n\n"
  TEXT += f"✰ **Pʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{ramdi}` \n\n"
  TEXT += "**🖤Tʜᴀɴᴋꜱ ꜰᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ʜᴇʀᴇ, ᴅᴀʀʟɪɴɢ🖤**"
  BUTTON = [[Button.url("🥀 Aᴅᴅ ᴍᴇ 🥀", "http://t.me/cutiepiexrobot?startgroup=new"), Button.url("♡ Sᴜᴩᴩᴏʀᴛ ♡", "https://t.me/itzmeanon")]]
  await tbot.send_file(event.chat_id, PHOTO, caption=TEXT,  buttons=BUTTON)
