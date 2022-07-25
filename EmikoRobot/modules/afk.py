#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiAFKBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiAFKBot/blob/master/LICENSE >
#
# All rights reserved.
#

import time

from pyrogram import filters
from pyrogram.types import Message

from EmikoRobot import app, BOT_USERNAME
from EmikoRobot.helper_extra.afk_mongo import add_afk, is_afk, remove_afk
from EmikoRobot.__main__ import get_readable_time


@app.on_message(filters.command(["afk", f"afk@{BOT_USERNAME}"]) & ~filters.edited)
async def active_afk(_, message: Message):
    if message.sender_chat:
        return
    user_id = message.from_user.id
    verifier, reasondb = await is_afk(user_id)
    if verifier:
        await remove_afk(user_id)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time((int(time.time() - timeafk)))
            if afktype == "text":
                send = await message.reply_text(
                    f"**{message.from_user.first_name}** ɪᴢ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}",
                    disable_web_page_preview=True,
                )
            if afktype == "text_reason":
                send = await message.reply_text(
                    f"**{message.from_user.first_name}** ɪᴢ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\nKʏᴜɴᴋɪ: `{reasonafk}`",
                    disable_web_page_preview=True,
                )
            if afktype == "animation":
                if str(reasonafk) == "None":
                    send =  await message.reply_animation(
                        data,
                        caption=f"**{message.from_user.first_name}** ɪᴢ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}",
                    )
                else:
                    send = await message.reply_animation(
                        data,
                        caption=f"**{message.from_user.first_name}** ɪᴢ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\nKʏᴜɴᴋɪ: `{reasonafk}`",
                    )
            if afktype == "photo":
                if str(reasonafk) == "None":
                    send = await message.reply_photo(
                        photo=f"downloads/{user_id}.jpg",
                        caption=f"**{message.from_user.first_name}** ɪᴢ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}",
                    )
                else:
                    send = await message.reply_photo(
                        photo=f"downloads/{user_id}.jpg",
                        caption=f"**{message.from_user.first_name}** ɪᴢ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\nKʏᴜɴᴋɪ: `{reasonafk}`",
                    )
        except Exception as e:
            send =  await message.reply_text(
                f"**{message.from_user.first_name}** ɪᴢ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ",
                disable_web_page_preview=True,
            )
        return
    if len(message.command) == 1 and not message.reply_to_message:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    elif len(message.command) > 1 and not message.reply_to_message:
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "text_reason",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }
    elif (
        len(message.command) == 1
        and message.reply_to_message.animation
    ):
        _data = message.reply_to_message.animation.file_id
        details = {
            "type": "animation",
            "time": time.time(),
            "data": _data,
            "reason": None,
        }
    elif (
        len(message.command) > 1
        and message.reply_to_message.animation
    ):
        _data = message.reply_to_message.animation.file_id
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "animation",
            "time": time.time(),
            "data": _data,
            "reason": _reason,
        }
    elif len(message.command) == 1 and message.reply_to_message.photo:
        await app.download_media(
            message.reply_to_message, file_name=f"{user_id}.jpg"
        )
        details = {
            "type": "photo",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    elif len(message.command) > 1 and message.reply_to_message.photo:
        await app.download_media(
            message.reply_to_message, file_name=f"{user_id}.jpg"
        )
        _reason = message.text.split(None, 1)[1].strip()
        details = {
            "type": "photo",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }
    elif (
        len(message.command) == 1 and message.reply_to_message.sticker
    ):
        if message.reply_to_message.sticker.is_animated:
            details = {
                "type": "text",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
        else:
            await app.download_media(
                message.reply_to_message, file_name=f"{user_id}.jpg"
            )
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
    elif (
        len(message.command) > 1 and message.reply_to_message.sticker
    ):
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        if message.reply_to_message.sticker.is_animated:
            details = {
                "type": "text_reason",
                "time": time.time(),
                "data": None,
                "reason": _reason,
            }
        else:
            await app.download_media(
                message.reply_to_message, file_name=f"{user_id}.jpg"
            )
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": _reason,
            }
    else:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }

    await add_afk(user_id, details)
    send = await message.reply_text(
        f"{message.from_user.first_name} ɪs ɴᴏᴡ ᴀғᴋ(Aᴡᴀʏ Fʀᴏᴍ Kᴇʏʙᴏᴀʀᴅ)!"
    )
    
__help__ = """
*Aᴡᴀʏ ғʀᴏᴍ ɢʀᴏᴜᴘ*
 ❍ /afk <reason>*:* Mᴀʀᴋ ʏᴏᴜʀsᴇʟғ ᴀs AFK (ᴀᴡᴀʏ ғʀᴏᴍ ᴋᴇʏʙᴏᴀʀᴅ).
Wʜᴇɴ ᴍᴀʀᴋᴇᴅ ᴀs AFK, ᴀɴʏ ᴍᴇɴᴛɪᴏɴs ᴡɪʟʟ ʙᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴡɪᴛʜ ᴀ ᴍsɢ ᴛᴏ sᴀʏ ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ!
"""

__mod_name__ = "Aғᴋ"
__command_list__ = ["afk"]
