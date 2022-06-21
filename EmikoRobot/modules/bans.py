import html
import random

from time import sleep
from telegram import (
    ParseMode,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.error import BadRequest
from telegram.ext import CallbackContext, Filters, CommandHandler, run_async, CallbackQueryHandler
from telegram.utils.helpers import mention_html
from typing import Optional, List
from telegram import TelegramError

import EmikoRobot.modules.sql.users_sql as sql
from EmikoRobot.modules.disable import DisableAbleCommandHandler
from EmikoRobot.modules.helper_funcs.filters import CustomFilters
from EmikoRobot import (
    DEV_USERS,
    LOGGER,
    OWNER_ID,
    DRAGONS,
    DEMONS,
    TIGERS,
    WOLVES,
    dispatcher,
)
from EmikoRobot.modules.helper_funcs.chat_status import (
    user_admin_no_reply,
    bot_admin,
    can_restrict,
    connection_status,
    is_user_admin,
    is_user_ban_protected,
    is_user_in_chat,
    user_admin,
    user_can_ban,
    can_delete,
    dev_plus,
)
from EmikoRobot.modules.helper_funcs.extraction import extract_user_and_text
from EmikoRobot.modules.helper_funcs.string_handling import extract_time
from EmikoRobot.modules.log_channel import gloggable, loggable



@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def ban(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot = context.bot
    args = context.args
    reason = ""
    if message.reply_to_message and message.reply_to_message.sender_chat:
        r = bot.ban_chat_sender_chat(chat_id=chat.id, sender_chat_id=message.reply_to_message.sender_chat.id)
        if r:
            message.reply_text("Cʜᴀɴɴᴇʟ {} ᴡᴀs ʙᴀɴɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ғʀᴏᴍ {}".format(
                html.escape(message.reply_to_message.sender_chat.title),
                html.escape(chat.title)
            ),
                parse_mode="html"
            )
        else:
            message.reply_text("Fᴀɪʟᴇᴅ ᴛᴏ ʙᴀɴ ᴄʜᴀɴɴᴇʟ")
        return

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("⚠️ Usᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ.")
        return log_message
    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "User not found":
            raise
        message.reply_text("Cᴀɴ'ᴛ sᴇᴇᴍs ᴛᴏ ғɪɴᴅ ᴛʜɪs ᴘᴇʀsᴏɴ.")
        return log_message
    if user_id == bot.id:
        message.reply_text("Oʜ ʏᴇᴀʜ, ʙᴀɴ ᴍʏsᴇʟғ, ɴᴏᴏʙ!")
        return log_message

    if is_user_ban_protected(chat, user_id, member) and user not in DEV_USERS:
        if user_id == OWNER_ID:
            message.reply_text("❤️ᴅᴇ, ʙᴀᴀᴘ ʜᴀɪɴ ᴡᴏʜ ᴍᴇʀᴇ, ᴜɴᴋᴏ ᴋᴀɪsᴇ ʀɪsᴋ ᴍᴇɪɴ ᴅᴀʟᴜ ʙᴀᴛᴀ?")
        elif user_id in DEV_USERS:
            message.reply_text("I ᴄᴀɴ'ᴛ ᴀɢᴀɪɴsᴛ ᴏᴜʀ ᴘʀɪɴᴄᴇ.")
        elif user_id in DRAGONS:
            message.reply_text(
                "Fɪɢʜᴛɪɴɢ ᴛʜɪs ᴇᴍᴘᴇʀᴏʀ ʜᴇʀᴇ ᴡɪʟʟ ᴘᴜᴛ ᴜsᴇʀ ʟɪᴠᴇs ᴀᴛ ʀɪsᴋ."
            )
        elif user_id in DEMONS:
            message.reply_text(
                "Bʀɪɴɢ ᴀɴ ᴏʀᴅᴇʀ ғʀᴏᴍ ᴄᴀᴘᴛᴀɪɴ ᴛᴏ ғɪɢʜᴛ ᴀ ᴀssɪsᴀɴ sᴇʀᴠᴀɴᴛ."
            )
        elif user_id in TIGERS:
            message.reply_text(
                "Bʀɪɴɢ ᴀɴ ᴏʀᴅᴇʀ ғʀᴏᴍ sᴏʟᴅɪᴇʀ ᴛᴏ ғɪɢʜᴛ ᴀ ʟᴀɴᴄᴇʀ sᴇʀᴠᴀɴᴛ."
            )
        elif user_id in WOLVES:
            message.reply_text("Tʀᴀᴅᴇʀ ᴀᴄᴄᴇss ᴍᴀᴋᴇ ᴛʜᴇᴍ ʙᴀɴ ɪᴍᴍᴜɴᴇ!")
        else:
            message.reply_text("⚠️ Cᴀɴɴᴏᴛ ʙᴀɴɴᴇᴅ ᴀᴅᴍɪɴ.")
        return log_message
    if message.text.startswith("/s"):
        silent = True
        if not can_delete(chat, context.bot.id):
            return ""
    else:
        silent = False
    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#{'S' if silent else ''}BANNED\n"
        f"<b>Aᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>Usᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )
    if reason:
        log += "<b>Rᴇᴀsᴏɴ:</b> {}".format(reason)

    try:
        chat.ban_member(user_id)

        if silent:
            if message.reply_to_message:
                message.reply_to_message.delete()
            message.delete()
            return log

        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        reply = (
            f"{mention_html(member.user.id, html.escape(member.user.first_name))} [<code>{member.user.id}</code>] Bᴀɴɴᴇᴅ."
        )
        if reason:
            reply += f"\nRᴇᴀsᴏɴ: {html.escape(reason)}"

        bot.sendMessage(
            chat.id,
            reply,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🔄  Uɴʙᴀɴ", callback_data=f"unbanb_unban={user_id}"
                        ),
                        InlineKeyboardButton(text="🗑️  Dᴇʟᴇᴛᴇ", callback_data="unbanb_del"),
                    ]
                ]
            ),
            parse_mode=ParseMode.HTML,
        )
        return log

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            if silent:
                return log
            message.reply_text("Bᴀɴɴᴇᴅ!", quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ERROR ʙᴀɴɴɪɴɢ ᴜsᴇʀ %s ɪɴ %s (%s) ᴅᴜᴇ ᴛᴏ %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("Uʜᴍ...ᴛʜᴀᴛ ᴅɪᴅɴ'ᴛ ᴡᴏʀᴋ...")

    return log_message


@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def temp_ban(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("⚠️ Usᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "User not found":
            raise
        message.reply_text("I ᴄᴀɴ'ᴛ sᴇᴇᴍs ᴛᴏ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ.")
        return log_message
    if user_id == bot.id:
        message.reply_text("I'ᴍ ɴᴏᴛ ɢᴏɴɴᴀ BAN ᴍʏsᴇʟғ, ᴡʜᴀᴛ ᴛʜᴇ ғ*ᴄᴋ ʙʀᴏ?")
        return log_message

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text("I ᴅᴏɴ'ᴛ ғᴇᴇʟ ʟɪᴋᴇ ɪᴛ.")
        return log_message

    if not reason:
        message.reply_text("Yᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴘᴇᴄɪғɪᴇᴅ ᴀ ᴛɪᴍᴇ ᴛᴏ ʙᴀɴ ᴛʜᴀᴛ ᴜsᴇʀ ғᴏʀ!")
        return log_message

    split_reason = reason.split(None, 1)

    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""
    bantime = extract_time(message, time_val)

    if not bantime:
        return log_message

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        "#TEMP BANNED\n"
        f"<b>Aᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>Usᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}\n"
        f"<b>Tɪᴍᴇ:</b> {time_val}"
    )
    if reason:
        log += "\nRᴇᴀsᴏɴ: {}".format(reason)

    try:
        chat.ban_member(user_id, until_date=bantime)
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker

        reply_msg = (
            f"{mention_html(member.user.id, html.escape(member.user.first_name))} [<code>{member.user.id}</code>] Tᴇᴍᴘᴏʀᴀʀʏ ʙᴀɴɴᴇᴅ"
            f" ғᴏʀ (`{time_val}`)."
        )

        if reason:
            reply_msg += f"\nRᴇᴀsᴏɴ: `{html.escape(reason)}`"

        bot.sendMessage(
            chat.id,
            reply_msg,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🔄  Uɴʙᴀɴ", callback_data=f"unbanb_unban={user_id}"
                        ),
                        InlineKeyboardButton(text="🗑️  Dᴇʟᴇᴛᴇ", callback_data="unbanb_del"),
                    ]
                ]
            ),
            parse_mode=ParseMode.HTML,
        )
        return log

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text(
                f"{mention_html(member.user.id, html.escape(member.user.first_name))} [<code>{member.user.id}</code>] ʙᴀɴɴᴇᴅ ғᴏʀ {time_val}.", quote=False
            )
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ERROR ʙᴀɴɴɪɴɢ ᴜsᴇʀ %s ɪɴ %s (%s) ᴅᴜᴇ ᴛᴏ %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("Wᴇʟʟ ᴅᴀᴍɴ, ɪ ᴄᴀɴ'ᴛ ʙᴀɴ ᴛʜᴀᴛ ᴜsᴇʀ.")

    return log_message


@connection_status
@bot_admin
@can_restrict
@user_admin_no_reply
@user_can_ban
@loggable
def unbanb_btn(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    query = update.callback_query
    chat = update.effective_chat
    user = update.effective_user
    if query.data != "unbanb_del":
        splitter = query.data.split("=")
        query_match = splitter[0]
        if query_match == "unbanb_unban":
            user_id = splitter[1]
            if not is_user_admin(chat, int(user.id)):
                bot.answer_callback_query(
                    query.id,
                    text="⚠️ Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛs ᴛᴏ ᴜɴᴍᴜᴛᴇ ᴘᴇᴏᴘʟᴇ",
                    show_alert=True,
                )
                return ""
            log_message = ""
            try:
                member = chat.get_member(user_id)
            except BadRequest:
                pass
            chat.unban_member(user_id)
            query.message.edit_text(
                f"{member.user.first_name} [{member.user.id}] Uɴʙᴀɴɴᴇᴅ."
            )
            bot.answer_callback_query(query.id, text="Unbanned!")
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#UNBANNED\n"
                f"<b>Aᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
                f"<b>Usᴇʀ:</b> {mention_html(member.user.id, member.user.first_name)}"
            )

    else:
        if not is_user_admin(chat, int(user.id)):
            bot.answer_callback_query(
                query.id,
                text="⚠️ Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛs ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴛʜɪs ᴍsɢ.",
                show_alert=True,
            )
            return ""
        query.message.delete()
        bot.answer_callback_query(query.id, text="Deleted!")
        return ""

    
@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def punch(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("⚠️ Usᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "User not found":
            raise

        message.reply_text("⚠️ I ᴄᴀɴ'ᴛ sᴇᴇᴍs ᴛᴏ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ.")
        return log_message
    if user_id == bot.id:
        message.reply_text("Yᴇᴀʜʜʜ. ɪ'ᴍ ɴᴏᴛ ɢᴏɪɴɢ ᴛᴏ ᴅᴏ ᴛʜᴀᴛ")
        return log_message

    if is_user_ban_protected(chat, user_id):
        message.reply_text("I ʀᴇᴀʟʟʏ ᴡɪsʜ ɪ ᴄᴏᴜʟᴅ ᴘᴜɴᴄʜ ᴛʜɪs ᴜsᴇʀ....")
        return log_message

    res = chat.unban_member(user_id)  # unban on current user = kick
    if res:
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        bot.sendMessage(
            chat.id,
            f"{mention_html(member.user.id, html.escape(member.user.first_name))} [<code>{member.user.id}</code>] Kɪᴄᴋᴇᴅ.",
            parse_mode=ParseMode.HTML
        )
        log = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#KICKED\n"
            f"<b>Aᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>Usᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
        )
        if reason:
            log += f"\n<b>Rᴇᴀsᴏɴ:</b> {reason}"

        return log

    else:
        message.reply_text("⚠️ Wᴇʟʟ ᴅᴀᴍɴ, ɪ ᴄᴀɴ'ᴛ ᴘᴜɴᴄʜ ᴛʜᴀᴛ ᴜsᴇʀ.")

    return log_message



@bot_admin
@can_restrict
def punchme(update: Update, context: CallbackContext):
    user_id = update.effective_message.from_user.id
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text("ᴀᴅᴍɪɴ ʜᴏᴋʀ ɴᴀᴛᴀᴋ ᴍᴛ ᴋʀ ᴠᴀᴀɪ.")
        return

    res = update.effective_chat.unban_member(user_id)  # unban on current user = kick
    if res:
        update.effective_message.reply_text(
            "ɴɪᴋᴀʟ ʙᴇᴛᴇ ʏʜᴀ sᴇ...!!",
        )
    else:
        update.effective_message.reply_text("Hᴜʜ? ɪ ᴄᴀɴ'ᴛ :/")


@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def unban(update: Update, context: CallbackContext) -> Optional[str]:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    log_message = ""
    bot, args = context.bot, context.args
    if message.reply_to_message and message.reply_to_message.sender_chat:
        r = bot.unban_chat_sender_chat(chat_id=chat.id, sender_chat_id=message.reply_to_message.sender_chat.id)
        if r:
            message.reply_text("Cʜᴀɴɴᴇʟ {} ᴡᴀs ʙᴀɴɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ғʀᴏᴍ {}".format(
                html.escape(message.reply_to_message.sender_chat.title),
                html.escape(chat.title)
            ),
                parse_mode="html"
            )
        else:
            message.reply_text("Fᴀɪʟᴇᴅ ᴛᴏ ᴜɴʙᴀɴ ᴄʜᴀɴɴᴇʟ")
        return

    user_id, reason = extract_user_and_text(message, args)
    if not user_id:
        message.reply_text("⚠️ Usᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "User not found":
            raise
        message.reply_text("I ᴄᴀɴ'ᴛ sᴇᴇᴍs ᴛᴏ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ.")
        return log_message
    if user_id == bot.id:
        message.reply_text("Hᴏᴡ ᴡᴏᴜʟᴅ ɪ ᴜɴʙᴀɴ ᴍʏsᴇʟғ ɪғ ɪ ᴡᴀsɴ'ᴛ ᴛʜᴇʀᴇ...?")
        return log_message

    if is_user_in_chat(chat, user_id):
        message.reply_text(f"⚠️ Usᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ.")
        return log_message

    chat.unban_member(user_id)
    message.reply_text(
        f"{member.user.first_name} [{member.user.id}] Uɴʙᴀɴɴᴇᴅ."
    )

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#UNBANNED\n"
        f"<b>Aᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>Usᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )
    if reason:
        log += f"\n<b>Rᴇᴀsᴏɴ:</b> {reason}"

    return log


@connection_status
@bot_admin
@can_restrict
@gloggable
def selfunban(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    bot, args = context.bot, context.args
    if user.id not in DRAGONS or user.id not in TIGERS:
        return

    try:
        chat_id = int(args[0])
    except:
        message.reply_text("Gɪᴍᴍᴇ ᴀ ᴠᴀʟɪᴅ ᴄʜᴀᴛ ID.")
        return

    chat = bot.getChat(chat_id)

    try:
        member = chat.get_member(user.id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("I ᴄᴀɴ'ᴛ sᴇᴇᴍs ᴛᴏ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ.")
            return
        else:
            raise

    if is_user_in_chat(chat, user.id):
        message.reply_text("Aʀᴇɴ'ᴛ ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ??")
        return

    chat.unban_member(user.id)
    message.reply_text(f"Yᴇᴘ, ɪ ʜᴀᴠᴇ ᴜɴʙᴀɴɴᴇᴅ ᴛʜᴇ ᴜsᴇʀ.")

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#UNBANNED\n"
        f"<b>Usᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )

    return log


@bot_admin
@can_restrict
@loggable
def banme(update: Update, context: CallbackContext):
    user_id = update.effective_message.from_user.id
    chat = update.effective_chat
    user = update.effective_user
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text("⚠️ I ᴄᴀɴ'ᴛ ʙᴀɴɴᴇᴅ ᴀᴅᴍɪɴ.")
        return

    res = update.effective_chat.ban_member(user_id)
    if res:
        update.effective_message.reply_text("Yᴇs, ʏᴘᴜ'ʀᴇ ʀɪɢʜᴛ! GTFO..")
        return (
            "<b>{}:</b>"
            "\n#BANME"
            "\n<b>Usᴇʀ:</b> {}"
            "\n<b>ID:</b> <code>{}</code>".format(
                html.escape(chat.title),
                mention_html(user.id, user.first_name),
                user_id,
            )
        )

    else:
        update.effective_message.reply_text("Hᴜʜ? ɪ ᴄᴀɴ'ᴛ' :/")


@dev_plus
def snipe(update: Update, context: CallbackContext):
    args = context.args
    bot = context.bot
    try:
        chat_id = str(args[0])
        del args[0]
    except TypeError:
        update.effective_message.reply_text("Pʟᴇᴀsᴇ ɢɪᴍᴍᴇ ᴀ ᴄʜᴀᴛ ᴛᴏ ᴇᴄʜᴏ ᴛᴏ!")
    to_send = " ".join(args)
    if len(to_send) >= 2:
        try:
            bot.sendMessage(int(chat_id), str(to_send))
        except TelegramError:
            LOGGER.warning("Cᴏᴜʟᴅɴ'ᴛ sᴇɴᴅ ᴛᴏ ɢʀᴏᴜᴘ %s", str(chat_id))
            update.effective_message.reply_text(
                "Cᴏᴜʟᴅɴ'ᴛ sᴇᴍᴅ ᴛʜᴇ ᴍsɢ. Pᴇʀʜᴀᴘs ɪ'ᴍ ɴᴏᴛ ᴏᴀʀᴛ ᴏғ ᴛʜᴀᴛ ɢʀᴏᴜᴘ?"
            )


__help__ = """
*ᑌՏᗴᖇ ᑕOᗰᗰᗩᑎᗪՏ:*
➻ /kickme*:* Kɪᴄᴋs ᴛʜᴇ ᴜsᴇʀ ᴡʜᴏ ᴜssᴜᴇᴅ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ.
*ᗩᗪᗰIᑎՏ OᑎᒪY:*
➻ /ban <userhandle>*:* Bᴀɴs ᴀ ᴜsᴇʀ.
➻ /sban <userhandle>*:* Sɪʟᴇɴᴛʟʏ ʙᴀɴs ᴀ ᴜsᴇʀ.
➻ /tban <userhandle> X(m/h/d)*:* Bᴀɴs ᴀ ᴜsᴇʀ ғᴏᴛ X ᴛɪᴍᴇ. m = minutes, h = hours, d = days.
➻ /unban <userhandle>*:* Uɴʙᴀɴs ᴀ ᴜsᴇʀ.
➻ /kick <userhandle>*:* Kɪᴄᴋs ᴀ ᴜsᴇʀ ᴏᴜᴛ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴘ.
➻ /mute <userhandle>*:* Sɪʟᴇɴᴄᴇs ᴀ ᴜsᴇʀ.
➻ /tmute <userhandle> X(m/h/d)*:* Mᴜᴛᴇs ᴀ ᴜsᴇʀ ғᴏʀ X ᴛɪᴍᴇ. m = minutes, h = hours, d = days.
➻ /unmute <userhandle>*:* Uɴᴍᴜᴛᴇs ᴀ ᴜsᴇʀ.
➻ /zombies*:* Sᴇᴀʀᴄʜᴇs ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs.
➻ /zombies clean*:* Rᴇᴍᴏᴠᴇs ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛᴀ ғʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ.
➻ /snipe <chatid> <string>*:* Mᴀᴋᴇ ᴍ sᴇɴᴅ ᴀ ᴍsɢ ᴛᴏ ᴀ sᴘᴇᴄɪғɪᴄ ᴄʜᴀᴛ.
"""


__mod_name__ = "Bᴀɴꜱ/Mᴜᴛᴇ"

BAN_HANDLER = CommandHandler(["ban", "sban"], ban, run_async=True)
TEMPBAN_HANDLER = CommandHandler(["tban"], temp_ban, run_async=True)
KICK_HANDLER = CommandHandler(["kick", "punch"], punch, run_async=True)
UNBAN_HANDLER = CommandHandler("unban", unban, run_async=True)
ROAR_HANDLER = CommandHandler("roar", selfunban, run_async=True)
UNBAN_BUTTON_HANDLER = CallbackQueryHandler(unbanb_btn, pattern=r"unbanb_")
KICKME_HANDLER = DisableAbleCommandHandler(["kickme", "punchme"], punchme, filters=Filters.chat_type.groups, run_async=True)
SNIPE_HANDLER = CommandHandler("snipe", snipe, pass_args=True, filters=CustomFilters.sudo_filter, run_async=True)
BANME_HANDLER = CommandHandler("banme", banme, run_async=True)

dispatcher.add_handler(BAN_HANDLER)
dispatcher.add_handler(TEMPBAN_HANDLER)
dispatcher.add_handler(KICK_HANDLER)
dispatcher.add_handler(UNBAN_HANDLER)
dispatcher.add_handler(ROAR_HANDLER)
dispatcher.add_handler(KICKME_HANDLER)
dispatcher.add_handler(UNBAN_BUTTON_HANDLER)
dispatcher.add_handler(SNIPE_HANDLER)
dispatcher.add_handler(BANME_HANDLER)

__handlers__ = [
    BAN_HANDLER,
    TEMPBAN_HANDLER,
    KICK_HANDLER,
    UNBAN_HANDLER,
    ROAR_HANDLER,
    KICKME_HANDLER,
    UNBAN_BUTTON_HANDLER,
    SNIPE_HANDLER,
    BANME_HANDLER,
]
