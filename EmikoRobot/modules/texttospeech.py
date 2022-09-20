import os

from gtts import gTTS
from gtts import gTTSError
from telethon import *
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *

from EmikoRobot import *

from EmikoRobot import telethn as tbot
from EmikoRobot.events import register


@register(pattern="^/tts (.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str
    elif "|" in input_str:
        lan, text = input_str.split("|")
    else:
        await event.reply(
            "Iɴᴠᴀʟɪᴅ sʏɴᴛᴀx⚠️\nFᴏʀᴍᴀᴛ `/tts lang | text`\nFᴏʀ ᴇɢ: `/tts en | hello`"
        )
        return
    text = text.strip()
    lan = lan.strip()
    try:
        tts = gTTS(text, tld="com", lang=lan)
        tts.save("k.mp3")
    except AssertionError:
        await event.reply(
            "Tʜᴇ ᴛᴇxᴛ ɪs ᴇᴍᴘᴛʏ.\n"
            "Nᴏᴛʜɪɴɢ ʟᴇғᴛ ᴛᴏ sᴘᴇᴀᴋ ᴀғᴛᴇʀ ᴘʀᴇ-ᴘʀᴇᴄᴇssɪɴɢ to speak after pre-precessing, "
            "ᴛᴏᴋᴇɴɪᴢɪɴɢ ᴀɴᴅ ᴄʟᴇᴀɴɪɴɢ."
        )
        return
    except ValueError:
        await event.reply("Lᴀɴɢᴜᴀɢᴇ ɪs ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ")
        return
    except RuntimeError:
        await event.reply("Eʀʀᴏʀ ʟᴏᴀᴅɪɴɢ ᴛʜᴇ ʟᴀɴɢᴜᴀɢᴇs ᴅɪᴄᴛɪᴏɴᴀʀʏ.")
        return
    except gTTSError:
        await event.reply("Eʀʀᴏʀ ɪɴ ɢᴏᴏɢʟᴇ `Text-to-Speech` API ʀᴇǫᴜᴇsᴛ !")
        return
    with open("k.mp3", "r"):
        await tbot.send_file(
            event.chat_id, "k.mp3", voice_note=True, reply_to=reply_to_id
        )
        os.remove("k.mp3")
