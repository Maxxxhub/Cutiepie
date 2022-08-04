import logging
import time

from pyrogram import filters
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    PeerIdInvalid,
    UsernameNotOccupied,
    UserNotParticipant,
)
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup

from EmikoRobot import DRAGONS as SUDO_USERS
from EmikoRobot import pbot
from EmikoRobot.modules.sql import forceSubscribe_sql as sql

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(
    lambda _, __, query: query.data == "onUnMuteRequest"
)


@pbot.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, cb):
    user_id = cb.from_user.id
    chat_id = cb.message.chat.id
    chat_db = sql.fs_settings(chat_id)
    if chat_db:
        channel = chat_db.channel
        chat_member = client.get_chat_member(chat_id, user_id)
        if chat_member.restricted_by:
            if chat_member.restricted_by.id == (client.get_me()).id:
                try:
                    client.get_chat_member(channel, user_id)
                    client.unban_chat_member(chat_id, user_id)
                    cb.message.delete()
                    # if cb.message.reply_to_message.from_user.id == user_id:
                    # cb.message.delete()
                except UserNotParticipant:
                    client.answer_callback_query(
                        cb.id,
                        text=f"❗ Jᴏɪɴ ᴏᴜʀ @{channel} ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴘʀᴇss  '✌️Uɴᴍᴜᴛᴇ ᴍᴇ✌️' ʙᴜᴛᴛᴏɴ.",
                        show_alert=True,
                    )
            else:
                client.answer_callback_query(
                    cb.id,
                    text="❗ Yᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ᴍᴜᴛᴇᴅ ʙʏ ᴀᴅᴍɪɴs ᴅᴜᴇ ᴛᴏ sᴏᴍᴇ ᴏᴛʜᴇʀ ʀᴇᴀsᴏɴ.",
                    show_alert=True,
                )
        else:
            if (not client.get_chat_member(chat_id, (client.get_me()).id).status == "administrator"
            ):
                client.send_message(
                    chat_id,
                    f"❗ **{cb.from_user.mention} ɪs ᴛʀʏɪɴɢ ᴛᴏ ᴜɴᴍᴜᴛᴇ ʜɪᴍsᴇʟғ ʙᴜᴛ ɪ ᴄᴀɴ'ᴛ ᴜɴᴍᴜᴛᴇ ʜɪᴍ ʙᴄᴏᴢ ɪ ᴀᴍ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ᴄʜᴀᴛ..Aᴅᴅ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ғɪʀsᴛ.**\n__#Lᴇᴀᴠɪɴɢ ᴛʜɪs ᴄʜᴀᴛ...__",
                )

            else:
                client.answer_callback_query(
                    cb.id,
                    text="❗ Wᴀʀɴɪɴɢ! Mᴀᴢᴇ ɴᴀʜ ʟᴇ ʙᴇᴛᴇ 🤨.",
                    show_alert=True,
                )


@pbot.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
    chat_id = message.chat.id
    chat_db = sql.fs_settings(chat_id)
    if chat_db:
        user_id = message.from_user.id
        if (not client.get_chat_member(chat_id, user_id).status in ("administrator", "creator")
            and not user_id in SUDO_USERS
        ):
            channel = chat_db.channel
            try:
                client.get_chat_member(channel, user_id)
            except UserNotParticipant:
                try:
                    sent_message = message.reply_text(
                        "Wᴇʟᴄᴏᴍᴇ ʙʀᴏᴛʜᴇʀ/sɪs {} 🙏 \n **Yᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ᴏᴜʀ @{} ᴄʜᴀɴɴᴇʟ ʏᴇᴛ**😕 \n \nJᴏɪɴ [Oᴜʀ ᴄʜᴀɴɴᴇʟ](https://t.me/{}) ᴀɴᴅ ʜɪᴛ ᴛʜᴀᴛ **✌️Uɴᴍᴜᴛᴇ ᴍᴇ✌️** Bᴜᴛᴛᴏɴ. \n \n ".format(
                            message.from_user.mention, channel, channel
                        ),
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "👉Jᴏɪɴ ᴄʜᴀɴɴᴇʟ👈",
                                        url="https://t.me/{}".format(channel),
                                    )
                                ],
                                [
                                    InlineKeyboardButton(
                                        "✌️Uɴᴍᴜᴛᴇ ᴍᴇ✌️", callback_data="onUnMuteRequest"
                                    )
                                ],
                            ]
                        ),
                    )
                    client.restrict_chat_member(
                        chat_id, user_id, ChatPermissions(can_send_messages=False)
                    )
                except ChatAdminRequired:
                    sent_message.edit(
                        "😕 **Tᴇᴅᴅʏ ɪs ɴᴏᴛ ᴀᴅᴍɪɴ ʜᴇʀᴇ..**\n__Mᴀᴋᴇ ᴛᴇᴅᴅʏ ᴀᴅᴍɪɴ ᴡɪᴛʜ ʙᴀɴ ʀɪɢʜᴛs ᴀɴᴅ ʀᴇᴛʀʏ.. \n#Eɴᴅɪɴɢ FSUB...__"
                    )

            except ChatAdminRequired:
                client.send_message(
                    chat_id,
                    text=f"😕 **I ᴀᴍ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ᴏғ @{channel} ᴄʜᴀɴɴᴇʟ.**\n__Mᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ ɪɴ @{channel} ᴀɴᴅ ʀᴇᴛʀʏ.\n#Eɴᴅɪɴɢ FSUB...__",
                )


@pbot.on_message(filters.command(["forcesubscribe", "fsub"]) & ~filters.private)
def config(client, message):
    user = client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status == "creator" or user.user.id in SUDO_USERS:
        chat_id = message.chat.id
        if len(message.command) > 1:
            input_str = message.command[1]
            input_str = input_str.replace("@", "")
            if input_str.lower() in ("off", "no", "disable"):
                sql.disapprove(chat_id)
                message.reply_text("❌ **Fᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ɪs ᴅɪsᴀʙʟᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.**")
            elif input_str.lower() in ("clear"):
                sent_message = message.reply_text(
                    "**Uɴᴍᴜᴛɪᴍɢ ᴀʟʟ ᴍᴇᴍʙᴇʀs ᴡʜᴏ ᴀʀᴇ ᴍᴜᴛᴇᴅ ʙʏ ᴍᴇ...**"
                )
                try:
                    for chat_member in client.get_chat_members(
                        message.chat.id, filter="restricted"
                    ):
                        if chat_member.restricted_by.id == (client.get_me()).id:
                            client.unban_chat_member(chat_id, chat_member.user.id)
                            time.sleep(1)
                    sent_message.edit("✅ **Uɴᴍᴜᴛᴇᴅ ᴀʟʟ ᴍᴇᴍʙᴇʀs ᴡʜᴏ ᴀʀᴇ ᴍᴜᴛᴇᴅ ʙʏ ᴍᴇ.**")
                except ChatAdminRequired:
                    sent_message.edit(
                        "😕 **I ᴀᴍ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.**\n__I ᴄᴀɴ'ᴛ ᴜɴᴍᴜᴛᴇ ᴍᴍʙᴇʀs ʙᴄᴏᴢ ɪ ᴀᴍ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ᴄʜᴀᴛ, ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴡᴏᴛʜ ʙᴀɴ ᴜsᴇʀ ᴘᴇʀᴍɪssɪᴏɴ.__"
                    )
            else:
                try:
                    client.get_chat_member(input_str, "me")
                    sql.add_channel(chat_id, input_str)
                    message.reply_text(
                        f"✅ **Fᴏʀᴄᴇ Sᴜʙsᴄʀɪʙᴇ ɪs ᴇɴᴀʙʟᴇᴅ**\n__Fᴏʀᴄᴇ Sᴜʙsᴄʀɪʙᴇ ɪs ᴇɴᴀʙʟᴇᴅ, ᴀʟʟ ᴛʜᴇ ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀsʜᴀᴠᴇ ᴛᴏ sᴜʙsᴄʀɪʙᴇ ᴛ [ᴄʜᴀɴɴᴇʟ](https://t.me/{input_str}) ɪɴ ᴏʀᴅᴇʀ ᴛᴏ sᴇᴍᴅ ᴍsɢ's ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.__",
                        disable_web_page_preview=True,
                    )
                except UserNotParticipant:
                    message.reply_text(
                        f"😕 **Nᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ**\n__I ᴀᴍ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ [ᴄʜᴀɴɴᴇʟ](https://t.me/{input_str}). Aᴅᴅ ᴍᴇ ᴀs ᴀ ᴀᴅᴍɪɴ ɪɴ ᴏʀᴅᴇʀ ᴛᴏ ᴇɴᴀʙʟᴇ ғsᴜʙ.__",
                        disable_web_page_preview=True,
                    )
                except (UsernameNotOccupied, PeerIdInvalid):
                    message.reply_text(f"❗ **Iɴᴠᴀʟɪᴅ ᴄʜᴀɴɴᴇʟ ᴜsᴇʀɴᴀᴍᴇ.**")
                except Exception as err:
                    message.reply_text(f"❗ **ERROR:** ```{err}```")
        else:
            if sql.fs_settings(chat_id):
                message.reply_text(
                    f"✅ **Fᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ɪs ᴇɴᴀʙʟᴇᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.**\n__Fᴏʀ ᴛʜɪs [ᴄʜᴀɴɴᴇʟ](https://t.me/{sql.fs_settings(chat_id).channel})__",
                    disable_web_page_preview=True,
                )
            else:
                message.reply_text("❌ **Fᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ɪs ᴅɪsᴀʙʟᴇᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.**")
    else:
        message.reply_text(
            "❗ **Gʀᴏᴜᴘ ᴄʀᴇᴀᴛᴘʀ ʀᴇǫᴜɪʀᴇᴅ**\n__Yᴏᴜ ʜᴀᴠᴇ ᴛᴏ ʙᴇ ᴛʜᴇ ɢʀᴏᴜᴘ ᴄʀᴇᴀᴛᴏʀ ᴛᴏ ᴅᴏ ᴛʜᴀᴛ!__"
        )


__help__ = """
*Fᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ:*
➻ I ᴄᴀɴ ᴍᴜᴛᴇ ᴍᴇᴍʙᴇʀs ᴡʜᴏ ᴀʀᴇ ɴᴏᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴜɴᴛɪʟ ᴛʜᴇʏ sᴜʙsᴄʀɪʙᴇ.
➻ Wʜᴇɴ ᴇɴᴀʙʟᴇᴅ ғsᴜʙ, ɪ ᴡɪʟʟ ᴍᴜᴛᴇ ᴜɴsᴜʙsᴄʀɪʙᴇᴅ ᴍᴇᴍʙᴇʀs ᴀɴᴅ sʜᴏᴡ ᴛʜᴇᴍ ᴀ ᴜɴᴍᴜᴛᴇ ʙᴜᴛᴛᴏɴ, Wʜᴇɴ ᴛʜᴇʏ ᴘʀᴇssᴇᴅ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ɪ ᴡɪʟʟ ᴜɴᴍᴜᴛᴇ ᴛʜᴇᴍ.
*✘ Sᴇᴛᴜᴘ ✘*
* ONLY CREATOR *
➻ Aᴅᴅ ᴍᴇ ɪɴ ᴜʀ ɢʀᴏᴜᴘ ᴀs ᴀᴅᴍɪɴ.
➻ Aᴅᴅ ᴍᴇ ɪɴ ᴜʀ ᴄʜᴀɴɴᴇʟ ᴀs ᴀᴅᴍɪɴ.
 
*✘ Cᴏᴍᴍᴀɴᴅs ✘*
➻ /fsub {ᴄʜᴀɴɴᴇʟ ᴜsᴇʀɴᴀᴍᴇ} - Tᴏ ᴛᴜʀɴ ᴏɴ ғsᴜʙ ᴀɴᴅ sᴇᴛᴜᴘ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ.
  💡Dᴏ ᴛʜɪs ғɪʀsᴛ...
➻ /fsub - Tᴏ ɢᴇᴛ ᴛʜᴇ ᴄᴜʀʀᴇᴍᴛ ғsᴜʙ sᴇᴛᴛɪɴɢs.
➻ /fsub disable - Tᴏ ᴛᴜʀɴ ᴏғғ ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ..
  💡Iғ ʏᴏᴜ ᴅɪsᴀʙʟᴇ ғsᴜʙ, ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ sᴇᴛ ᴀɢᴀɪɴ ғᴏʀ ᴡᴏʀᴋɪɴɢ.. /fsub {ᴄʜᴀɴɴᴇʟ ᴜsᴇʀɴᴀᴍᴇ} 
➻ /fsub clear - Tᴏ ᴜɴᴍᴜᴛᴇ ᴀʟʟ ᴍᴇᴍʙᴇʀs ᴡʜᴏ ᴍᴜᴛᴇᴅ ʙʏ ᴍᴇ.
"""
__mod_name__ = "F-sᴜʙ"
