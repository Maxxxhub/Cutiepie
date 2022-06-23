from gpytranslate import Translator
from telegram.ext import CommandHandler, CallbackContext
from telegram import (
    Message,
    Chat,
    User,
    ParseMode,
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from EmikoRobot import dispatcher, pbot
from pyrogram import filters
from EmikoRobot.modules.disable import DisableAbleCommandHandler


__help__ = """ 
Tʜɪs ᴍᴏᴅᴜʟᴇ ᴡɪʟʟ ʜᴇʟᴘ.ʏᴏᴜ ɪɴ ᴛʀᴀɴsʟᴀᴛɪᴏɴ!
*✘ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀 ✘:*
➻ /tl (or /tr): As ᴀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ, ᴛʀᴀɴsʟᴀᴛᴇs ɪᴛ ᴛᴏ ᴇɴɢʟɪsʜ.
➻ /tl <lang>: Tʀᴀɴsʟᴀᴛᴇs ᴛᴏ <ʟᴀɴɢ ᴄᴏᴅᴇ>
eg: /tl en: Tʀᴀɴsʟᴀᴛᴇs ᴛᴏ ᴇɴɢʟɪsʜ.
➻ /tl <source>//<dest>: Tʀᴀɴsʟᴀᴛᴇs ғʀᴏᴍ <source> ᴛᴏ <lang>.
ᴇɢ:  /tl ja//en: Tʀᴀɴsʟᴀᴛᴇs ғʀᴏᴍ ᴊᴀᴘᴀɴᴇsᴇ ᴛᴏ ᴇɴɢʟɪsʜ.
➻ /langs: Gᴇᴛ ᴀ ʟɪsᴛ ᴏғ sᴜᴘᴘᴏʀᴛᴇᴅ ʟᴀɴɢᴜᴀɢᴇs ғᴏʀ ᴛʀᴀɴsʟᴀᴛɪᴏɴ.
I ᴄᴀɴ ᴄᴏɴᴠᴇʀᴛ ᴛᴏ ᴛᴇxᴛ ᴛᴏ ᴠᴏɪᴄᴇ ᴀɴᴅ ᴠᴏɪᴄᴇ ᴛᴏ ᴛᴇxᴛ.
➻ /tts <lang code>*:* Rᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴍsɢ ᴛᴏ ɢᴇᴛ ᴛᴇxᴛ ᴛᴏ sᴘᴇᴇᴄʜ ᴏᴜᴛᴘᴜᴛ.
➻ /stt*:* Tʏᴘᴇ ɪɴ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴠᴏɪᴄᴇ ᴍsɢ (sᴜᴘᴘᴏʀᴛ ᴇɴɢ ᴏɴʟʏ) ᴛᴏ ᴇxᴛʀᴀᴄᴛ ᴛᴇxᴛ ғʀᴏᴍ ɪᴛ.
*✘ [Cʟɪᴄᴋ ʜᴇʀᴇ ғᴏʀ ʟᴀɴɢᴜᴀɢᴇ ᴄᴏᴅᴇs](https://t.me/Teddy_bot_updates/73) ✘*
"""

__mod_name__ = "Tʀᴀɴꜱʟᴀᴛᴏʀ"


trans = Translator()


@pbot.on_message(filters.command(["tl", "tr"]))
async def translate(_, message: Message) -> None:
    reply_msg = message.reply_to_message
    if not reply_msg:
        await message.reply_text("Rᴇᴘʟʏ ᴛᴏ ᴀ ᴍsɢ ᴛᴏ ᴛʀᴀɴsʟᴀᴛᴇ ɪᴛ!")
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        dest = "en"
    translation = await trans(to_translate, sourcelang=source, targetlang=dest)
    reply = (
        f"<b>Tʀᴀɴsʟᴀᴛᴇᴅ ғʀᴏᴍ {source} ᴛᴏ {dest}</b>:\n"
        f"<code>{translation.text}</code>"
    )

    await message.reply_text(reply, parse_mode="html")


def languages(update: Update, context: CallbackContext) -> None:
    update.effective_message.reply_text(
        "Cʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ sᴇᴇ ᴛʜᴇ ʟɪsᴛ ᴏғ sᴜᴘᴘᴏʀᴛᴇᴅ ʟᴀɴɢᴜᴀɢᴇ ᴄᴏᴅᴇs.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=" 🗽Lᴀɴɢᴜᴀɢᴇ ᴄᴏᴅᴇs 🗽",
                        url="https://t.me/Teddy_bot_updates/73",
                    ),
                ],
            ],
            disable_web_page_preview=True,
        ),
    )


LANG_HANDLER = DisableAbleCommandHandler("langs", languages, run_async=True)

dispatcher.add_handler(LANG_HANDLER)
