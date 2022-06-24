from telethon import events, Button, custom, version
from telethon.tl.types import ChannelParticipantsAdmins
import asyncio
import os,re
import requests
import datetime
import time
from datetime import datetime
import random
from PIL import Image
from io import BytesIO
from EmikoRobot import telethn as bot
from EmikoRobot import telethn as tgbot
from EmikoRobot.events import register
from EmikoRobot import dispatcher


edit_time = 5
""" =======================TEDDY ROBOT====================== """
file1 = "https://telegra.ph/file/9a85d0a873e2dd80d278d.jpg"
file2 = "https://telegra.ph/file/9e7815284031452afa9e5.jpg"
file3 = "https://telegra.ph/file/dcc5e003287f69acea368.jpg"
file4 = "https://telegra.ph/file/ed1ce7fee94f46b0f671e.jpg"
file5 = "https://telegra.ph/file/701028ce085ecfa961a36.jpg"
""" =======================TEDDY ROBOT====================== """


@register(pattern="/myinfo")
async def proboyx(event):
    chat = await event.get_chat()
    current_time = datetime.utcnow()
    firstname = event.sender.first_name
    button = [[custom.Button.inline("𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻",data="informations")]]
    on = await bot.send_file(event.chat_id, file=file2,caption= f"ʜᴇy {firstname}, \n ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ \n ᴛᴏ ɢᴇᴛ ɪɴꜰᴏ ᴀʙᴏᴜᴛ yᴏᴜ", buttons=button)

    await asyncio.sleep(edit_time)
    ok = await bot.edit_message(event.chat_id, on, file=file3, buttons=button) 

    await asyncio.sleep(edit_time)
    ok2 = await bot.edit_message(event.chat_id, ok, file=file5, buttons=button)

    await asyncio.sleep(edit_time)
    ok3 = await bot.edit_message(event.chat_id, ok2, file=file1, buttons=button)

    await asyncio.sleep(edit_time)
    ok7 = await bot.edit_message(event.chat_id, ok6, file=file4, buttons=button)
    
    await asyncio.sleep(edit_time)
    ok4 = await bot.edit_message(event.chat_id, ok3, file=file2, buttons=button)
    
    await asyncio.sleep(edit_time)
    ok5 = await bot.edit_message(event.chat_id, ok4, file=file1, buttons=button)
    
    await asyncio.sleep(edit_time)
    ok6 = await bot.edit_message(event.chat_id, ok5, file=file3, buttons=button)
    
    await asyncio.sleep(edit_time)
    ok7 = await bot.edit_message(event.chat_id, ok6, file=file5, buttons=button)

    await asyncio.sleep(edit_time)
    ok7 = await bot.edit_message(event.chat_id, ok6, file=file4, buttons=button)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"information")))
async def callback_query_handler(event):
  try:
    boy = event.sender_id
    PRO = await bot.get_entity(boy)
    LILIE = "𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗯𝘆 𝗧𝗲𝗱𝗱𝘆 \n\n"
    LILIE += f"Fɪʀsᴛ ɴᴀᴍᴇ : {PRO.first_name} \n"
    LILIE += f"Lᴀsᴛ ɴᴀᴍᴇ : {PRO.last_name}\n"
    LILIE += f"Yᴏᴜ ʙᴏᴛ : {PRO.bot} \n"
    LILIE += f"Rᴇsᴛʀɪᴄᴛᴇᴅ : {PRO.restricted} \n"
    LILIE += f"Usᴇʀ ID : {boy}\n"
    LILIE += f"Usᴇʀɴᴀᴍᴇ : {PRO.username}\n"
    await event.answer(LILIE, alert=True)
  except Exception as e:
    await event.reply(f"{e}")


__command_list__ = [
    "myinfo"
]
