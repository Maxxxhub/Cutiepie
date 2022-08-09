from pyrogram import filters

from EmikoRobot import pbot


@pbot.on_message(filters.command("write"))
async def handwriting(_, message):
    if len(message.command) < 2:
        return await message.reply_text("» ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴡʀɪᴛᴇ ɪᴛ ᴏɴ ᴍʏ ᴄᴏᴩʏ...")
    m = await message.reply_text("» ᴡᴀɪᴛ ᴀ sᴇᴄ, ʟᴇᴛ ᴍᴇ ᴡʀɪᴛᴇ ᴛʜᴀᴛ ᴛᴇxᴛ...")
    name = (
        message.text.split(None, 1)[1]
        if len(message.command) < 3
        else message.text.split(None, 1)[1].replace(" ", "%20")
    )
    hand = "https://apis.xditya.me/write?text=" + name
    await m.edit("» ᴜᴩʟᴏᴀᴅɪɴɢ...")
    await pbot.send_chat_action(message.chat.id, "upload_photo")
    await message.reply_photo(hand, caption="ᴡʀɪᴛᴛᴇɴ ᴡɪᴛʜ 🖊 ʙʏ [Cᴜᴛɪᴇᴘɪᴇ](t.me/itzmeanon)")
    
__help__ = """
✰ Wʀɪᴛᴇ ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ ᴏɴ ᴀ ᴡʜᴏᴛᴇ ᴘᴀɢᴇ ᴡɪᴛʜ ᴀ ᴘᴇɴ 🖊

×  /write <text> : Wʀɪᴛᴇs ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ ᴏɴ ᴀ ᴘᴀᴘᴇʀ
"""

__mod_name__ = "Wʀɪᴛᴇ"

