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
        return await message.reply_text("`Rᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴍsɢ ᴛᴏ ᴍᴀᴋᴇ ᴄᴀʀʙᴏɴ.`")
    if not message.reply_to_message.text:
        return await message.reply_text("`Rᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴍsɢ ᴛᴏ ᴍᴀᴋᴇ ᴄᴀʀʙᴏɴ.`")
    m = await message.reply_text("`Pʀᴇᴘᴀʀɪɴɢ ᴄᴀʀʙᴏɴ`")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("`Uᴘʟᴏᴀᴅɪɴɢ`")
    await pbot.send_photo(message.chat.id, carbon)
    await m.delete()
    carbon.close()


MEMEK = "https://telegra.ph/file/c18f3d06a999cd1839312.jpg"

@pbot.on_message(filters.command("repo"))
async def repo(_, message):
    await message.reply_photo(
        photo=MEMEK,
        caption=f"""✨ **Hᴇy, I'ᴍ Tᴇᴅᴅy Rᴏʙᴏᴛ** \n\n"
**Oᴡɴᴇʀ ʀᴇᴩᴏ : [Sᴜʀᴜ](https://t.me/smokerr_xd)** \n\n"
**Pyᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ :** `{y()}` \n\n"
**Lɪʙʀᴀʀy ᴠᴇʀꜱɪᴏɴ :** `{o}` \n\n"
**Tᴇʟᴇᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ :** `{s}` \n\n"
**Pyʀᴏɢʀᴀᴍ ᴠᴇʀꜱɪᴏɴ :** `{z}` \n\n"
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
