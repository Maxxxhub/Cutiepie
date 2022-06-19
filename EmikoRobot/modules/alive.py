import os
import re
from platform import python_version as kontol
from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from EmikoRobot.events import register
from EmikoRobot import telethn as tbot

PHOTO = "https://telegra.ph/file/00d5abf609557589c8d72.jpg"
@register(pattern=("/alive", "/teddy"))
async def awake(event):
  TEXT = f"**ʜɪɪ [{event.sender.first_name}](tg://user?id={event.sender.id}),『 ɪ'ᴍ ᴛᴇᴅᴅy ʀᴏʙᴏᴛ 』** \n\n"
  TEXT += "⚪ **ɪ'ᴍ ᴡᴏʀᴋɪɴɢ ᴩʀᴏᴩᴇʀʟy** \n\n"
  TEXT += f"⚪ **ᴍy ᴍᴀꜱᴛᴇʀ : [ꜱᴜʀᴜ](https://t.me/smokerr_xd)** \n\n"
  TEXT += f"⚪ **ʟɪʙʀᴀʀy ᴠᴇʀꜱɪᴏɴ :** `{telever}` \n\n"
  TEXT += f"⚪ **ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ :** `{tlhver}` \n\n"
  TEXT += f"⚪ **ᴩyʀᴏɢʀᴀᴍ ᴠᴇʀꜱɪᴏɴ :** `{pyrover}` \n\n"
  TEXT += "**ᴛʜᴀɴᴋꜱ ꜰᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ʜᴇʀᴇ, ᴅᴀʀʟɪɴɢ❤️**"
  BUTTON = [[Button.url(" ♡ Hᴇʟᴩ ♡", "https://t.me/Teddyrobot_bot?start=help"), Button.url("♡ Sᴜᴩᴩᴏʀᴛ ♡", "https://t.me/teddysupport")]]
  await tbot.send_file(event.chat_id, PHOTO, caption=TEXT,  buttons=BUTTON)
