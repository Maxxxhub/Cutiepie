import os
import re
from platform import python_version as kontol
from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from EmikoRobot.events import register
from EmikoRobot import telethn as tbot

PHOTO = "https://telegra.ph/file/fb69bf46ff817654d95af.jpg"
@register(pattern=("/alive"))
async def awake(event):
  TEXT = f"**ʜɪɪ [{event.sender.first_name}](tg://user?id={event.sender.id}),『 ɪ'ᴍ ᴛᴇᴅᴅy 』** \n\n"
  TEXT += "✰**I'ᴍ ᴡᴏʀᴋɪɴɢ ᴩʀᴏᴩᴇʀʟy** \n\n"
  TEXT += f"✰ **My ᴍᴀꜱᴛᴇʀ : [ꜱᴜʀᴜ](https://t.me/smokerr_xd)** \n\n"
  TEXT += f"✰ **Lɪʙʀᴀʀy ᴠᴇʀꜱɪᴏɴ :** `{telever}` \n\n"
  TEXT += f"✰**Tᴇʟᴇᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ :** `{tlhver}` \n\n"
  TEXT += f"✰ **Pyʀᴏɢʀᴀᴍ ᴠᴇʀꜱɪᴏɴ :** `{pyrover}` \n\n"
  TEXT += "**🖤Tʜᴀɴᴋꜱ ꜰᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ʜᴇʀᴇ, ᴅᴀʀʟɪɴɢ🖤**"
  BUTTON = [[Button.url("➕ Aᴅᴅ ᴛᴇᴅᴅʏ ➕", "http://t.me/Teddyrobot_bot?startgroup=new"), Button.url("♡ Sᴜᴩᴩᴏʀᴛ ♡", "https://t.me/teddysupport")]]
  await tbot.send_file(event.chat_id, PHOTO, caption=TEXT,  buttons=BUTTON)
