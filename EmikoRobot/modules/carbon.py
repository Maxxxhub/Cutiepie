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


MEMEK = "https://telegra.ph/file/76a907d00640f38f6d5fb.mp4"

@pbot.on_message(filters.command("repo"))
async def repo(_, message):
    await message.reply_video(
        video=MEMEK,
        caption=f"""✨ **Hᴇy, I'ᴍ Tᴇᴅᴅy Rᴏʙᴏᴛ** \n"
**Oᴡɴᴇʀ ʀᴇᴩᴏ : [Sᴜʀᴜ](https://t.me/smokerr_xd)** \n"
**Pyᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ :** `{y()}` \n"
**Lɪʙʀᴀʀy ᴠᴇʀꜱɪᴏɴ :** `{o}` \n"
**Tᴇʟᴇᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ :** `{s}` \n"
**Pyʀᴏɢʀᴀᴍ ᴠᴇʀꜱɪᴏɴ :** `{z}` \n"
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
    
__help__ = """
✘ ᴍᴀᴋᴇs ᴀ ᴄᴀʀʙᴏɴ ᴏғ ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ ᴀɴᴅ sᴇɴᴅ ɪᴛ ᴛᴏ ʏᴏᴜ.

× /carbon : ᴍᴀᴋᴇs ᴄᴀʀʙᴏɴ ɪғ ʀᴇᴩʟɪᴇᴅ ᴛᴏ ᴀ ᴛᴇxᴛ """

__mod_name__ = "Cᴀʀʙᴏɴ"
