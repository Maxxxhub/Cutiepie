from platform import python_version as y
from telegram import __version__ as o
from pyrogram import __version__ as z
from telethon import __version__ as s
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters
from EmikoRobot import pbot
from EmikoRobot.utils.errors import capture_err
from EmikoRobot.utils.functions import make_carbon


@pbot.on_message(filters.command("carbon"))
@capture_err
async def carbon_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text("`Reply to a text message to make carbon.`")
    if not message.reply_to_message.text:
        return await message.reply_text("`Reply to a text message to make carbon.`")
    m = await message.reply_text("`Preparing Carbon`")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("`Uploading`")
    await pbot.send_photo(message.chat.id, carbon)
    await m.delete()
    carbon.close()


MEMEK = "https://te.legra.ph/file/f4c942f18d17650efa0c2.jpg"

@pbot.on_message(filters.command("repo"))
async def repo(_, message):
    await message.reply_photo(
        photo=MEMEK,
        caption=f"""✨ **Hᴇy, ɪ'ᴍ ᴛᴇᴅᴅy ʀᴏʙᴏᴛ** 
**Oᴡɴᴇʀ ʀᴇᴩᴏ : [Suru](https://t.me/smokerr_xd)**
**Pyᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ :** `{y()}`
**Lɪʙʀᴀʀy ᴠᴇʀꜱɪᴏɴ :** `{o}`
**Tᴇʟᴇᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ :** `{s}`
**Pyʀᴏɢʀᴀᴍ ᴠᴇʀꜱɪᴏɴ :** `{z}`
**🙂.**
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📍 Rᴇᴩᴏ 📍", url="https://t.me/smokerr_xd"), 
                    InlineKeyboardButton(
                        "📍 Sᴜᴩᴩᴏʀᴛ 📍", url="https://t.me/teddysupport")
                ]
            ]
        )
    )
