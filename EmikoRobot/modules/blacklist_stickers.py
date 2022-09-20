import html
from typing import Optional

import EmikoRobot.modules.sql.blsticker_sql as sql
from EmikoRobot import LOGGER, dispatcher
from EmikoRobot.modules.connection import connected
from EmikoRobot.modules.disable import DisableAbleCommandHandler
from EmikoRobot.modules.helper_funcs.alternate import send_message
from EmikoRobot.modules.helper_funcs.chat_status import user_admin, user_not_admin
from EmikoRobot.modules.helper_funcs.misc import split_message
from EmikoRobot.modules.helper_funcs.string_handling import extract_time

from EmikoRobot.modules.log_channel import loggable
from EmikoRobot.modules.warns import warn
from telegram import Chat, Message, ParseMode, Update, User, ChatPermissions
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler
from telegram.utils.helpers import mention_html, mention_markdown


def blackliststicker(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    bot, args = context.bot, context.args
    conn = connected(bot, update, chat, user.id, need_admin=False)
    if conn:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if chat.type == "private":
            return
        chat_id = update.effective_chat.id
        chat_name = chat.title

    sticker_list = "<b>Lɪsᴛ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ sᴛɪᴄᴋᴇʀs ᴄᴜʀʀᴇɴᴛʟʏ ɪɴ {}:</b>\n".format(
        chat_name,
    )

    all_stickerlist = sql.get_chat_stickers(chat_id)

    if len(args) > 0 and args[0].lower() == "copy":
        for trigger in all_stickerlist:
            sticker_list += "<code>{}</code>\n".format(html.escape(trigger))
    elif len(args) == 0:
        for trigger in all_stickerlist:
            sticker_list += " - <code>{}</code>\n".format(html.escape(trigger))

    split_text = split_message(sticker_list)
    for text in split_text:
        if (
            sticker_list
            == "<b>Lɪsᴛ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ sᴛɪᴄᴋᴇʀs ᴄᴜʀʀᴇɴᴛʟʏ ɪɴ {}:</b>\n".format(
                chat_name,
            ).format(html.escape(chat_name))
        ):
            send_message(
                update.effective_message,
                "Tʜᴇʀᴇ ᴡᴇʀᴇ ɴᴏ ʙʟᴀᴄᴋʟɪsᴛ sᴛɪᴄᴋᴇʀs ɪɴ <b>{}</b>!".format(
                    html.escape(chat_name),
                ),
                parse_mode=ParseMode.HTML,
            )
            return
    send_message(update.effective_message, text, parse_mode=ParseMode.HTML)


@user_admin
def add_blackliststicker(update: Update, context: CallbackContext):
    bot = context.bot
    msg = update.effective_message  # type: Optional[Message]
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    words = msg.text.split(None, 1)
    bot = context.bot
    conn = connected(bot, update, chat, user.id)
    if conn:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            return
        chat_name = chat.title

    if len(words) > 1:
        text = words[1].replace("https://t.me/addstickers/", "")
        to_blacklist = list(
            {trigger.strip() for trigger in text.split("\n") if trigger.strip()},
        )

        added = 0
        for trigger in to_blacklist:
            try:
                get = bot.getStickerSet(trigger)
                sql.add_to_stickers(chat_id, trigger.lower())
                added += 1
            except BadRequest:
                send_message(
                    update.effective_message,
                    "Sᴛɪᴄᴋᴇʀ `{}` ᴄᴀɴ ɴᴏᴛ ʙᴇ ғᴏᴜɴᴅ!".format(trigger),
                    parse_mode="markdown",
                )

        if added == 0:
            return

        if len(to_blacklist) == 1:
            send_message(
                update.effective_message,
                "Sᴛɪᴄᴋᴇʀ <code>{}</code> ᴀᴅᴅᴇᴅ ᴛᴏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ sᴛɪᴄᴋᴇʀ ɪɴ <b>{}</b>!".format(
                    html.escape(to_blacklist[0]),
                    html.escape(chat_name),
                ),
                parse_mode=ParseMode.HTML,
            )
        else:
            send_message(
                update.effective_message,
                "<code>{}</code> sᴛɪᴄᴋᴇʀs ᴀᴅᴅᴇᴅ ᴛᴏ ʙʟᴀᴄᴋʟɪsᴛ sᴛɪᴄᴋᴇʀ ʟɪsᴛ ɪɴ <b>{}</b>!".format(
                    added,
                    html.escape(chat_name),
                ),
                parse_mode=ParseMode.HTML,
            )
    elif msg.reply_to_message:
        added = 0
        trigger = msg.reply_to_message.sticker.set_name
        if trigger is None:
            send_message(update.effective_message, "Sᴛɪᴄᴋᴇʀ ɪs ɪɴᴠᴀʟɪᴅ!")
            return
        try:
            get = bot.getStickerSet(trigger)
            sql.add_to_stickers(chat_id, trigger.lower())
            added += 1
        except BadRequest:
            send_message(
                update.effective_message,
                "Sᴛɪᴄᴋᴇʀ `{}` ᴄᴀɴ ɴᴏᴛ ʙᴇ ғᴏᴜɴᴅ!".format(trigger),
                parse_mode="markdown",
            )

        if added == 0:
            return

        send_message(
            update.effective_message,
            "Sᴛɪᴄʟᴇʀ <code>{}</code> ᴀᴅᴅᴇᴅ ᴛᴏ ʙʟᴀᴄᴋʟɪsᴛ sᴛɪᴄᴋᴇʀs ɪɴ <b>{}</b>!".format(
                trigger,
                html.escape(chat_name),
            ),
            parse_mode=ParseMode.HTML,
        )
    else:
        send_message(
            update.effective_message,
            "Tᴇʟʟ ᴍᴇ ᴡʜᴀᴛ sᴛɪᴄᴋᴇʀs ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴀᴅᴅ ᴍᴇ ᴛᴏ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ sᴛɪᴄᴋᴇʀs.",
        )


@user_admin
def unblackliststicker(update: Update, context: CallbackContext):
    bot = context.bot
    msg = update.effective_message  # type: Optional[Message]
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    words = msg.text.split(None, 1)
    bot = context.bot
    conn = connected(bot, update, chat, user.id)
    if conn:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            return
        chat_name = chat.title

    if len(words) > 1:
        text = words[1].replace("https://t.me/addstickers/", "")
        to_unblacklist = list(
            {trigger.strip() for trigger in text.split("\n") if trigger.strip()},
        )

        successful = 0
        for trigger in to_unblacklist:
            success = sql.rm_from_stickers(chat_id, trigger.lower())
            if success:
                successful += 1

        if len(to_unblacklist) == 1:
            if successful:
                send_message(
                    update.effective_message,
                    "Sᴛɪᴄᴋᴇʀ <code>{}</code> ᴅᴇʟᴇᴛᴇᴅ ғʀᴏᴍ.ʙʟᴀᴄᴋʟɪsᴛ ɪɴ <b>{}</b>!".format(
                        html.escape(to_unblacklist[0]),
                        html.escape(chat_name),
                    ),
                    parse_mode=ParseMode.HTML,
                )
            else:
                send_message(
                    update.effective_message,
                    "Tʜɪs sᴛɪᴄᴋᴇʀ ɪs ɴᴏᴛ ᴏɴ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ sᴛɪᴄᴋᴇʀ ʟɪsᴛ...!",
                )

        elif successful == len(to_unblacklist):
            send_message(
                update.effective_message,
                "Sᴛɪᴄᴋᴇʀ <code>{}</code> ᴅᴇʟᴇᴛᴇᴅ ғʀᴏᴍ ʙʟᴀᴄᴋʟɪsᴛ ɪɴ <b>{}</b>!".format(
                    successful,
                    html.escape(chat_name),
                ),
                parse_mode=ParseMode.HTML,
            )

        elif not successful:
            send_message(
                update.effective_message,
                "Nᴏɴᴇ ᴏғ ᴛʜᴇsᴇ sᴛɪᴄᴋᴇʀs ᴇxɪsᴛ, sᴏ ᴛʜᴇʏ ᴄᴀɴɴᴏᴛ ʙᴇ ʀᴇᴍᴏᴠᴇᴅ.",
                parse_mode=ParseMode.HTML,
            )

        else:
            send_message(
                update.effective_message,
                "Sᴛɪᴄᴋᴇʀ <code>{}</code> ᴅᴇʟᴇᴛᴇᴅ ғʀᴏᴍ ʙʟᴀᴄᴋʟɪsᴛ . {} ᴅɪᴅ ɴᴏᴛ ᴇxɪsᴛ, sᴏ ɪᴛ's ɴᴏᴛ ᴅᴇʟᴇᴛᴇᴅ.".format(
                    successful,
                    len(to_unblacklist) - successful,
                ),
                parse_mode=ParseMode.HTML,
            )
    elif msg.reply_to_message:
        trigger = msg.reply_to_message.sticker.set_name
        if trigger is None:
            send_message(update.effective_message, "Sticker is invalid!")
            return
        success = sql.rm_from_stickers(chat_id, trigger.lower())

        if success:
            send_message(
                update.effective_message,
                "Sᴛɪᴄᴋᴇʀ <code>{}</code> ᴅᴇʟᴇᴛᴇᴅ ғʀᴏᴍ ʙʟᴀᴄᴋʟɪsᴛ ɪɴ <b>{}</b>!".format(
                    trigger,
                    chat_name,
                ),
                parse_mode=ParseMode.HTML,
            )
        else:
            send_message(
                update.effective_message,
                "{} ɴᴏᴛ ғᴏᴜɴᴅ ᴏɴ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ sᴛɪᴄᴋᴇʀs...!".format(trigger),
            )
    else:
        send_message(
            update.effective_message,
            "Tᴇʟʟ ᴍᴇ ᴡʜᴀᴛ sᴛɪᴄᴋᴇʀs ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴀᴅᴅ ᴛᴏ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ sᴛɪᴄᴋᴇʀs.!",
        )


@loggable
@user_admin
def blacklist_mode(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]
    bot, args = context.bot, context.args
    conn = connected(bot, update, chat, user.id, need_admin=True)
    if conn:
        chat = dispatcher.bot.getChat(conn)
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if update.effective_message.chat.type == "private":
            send_message(
                update.effective_message,
                "Yᴏᴜ ᴄᴀɴ ᴏɴʟʏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘs.!",
            )
            return ""
        chat = update.effective_chat
        chat_id = update.effective_chat.id
        chat_name = update.effective_message.chat.title

    if args:
        if args[0].lower() in ["off", "nothing", "no"]:
            settypeblacklist = "turn off"
            sql.set_blacklist_strength(chat_id, 0, "0")
        elif args[0].lower() in ["del", "delete"]:
            settypeblacklist = "left, the message will be deleted"
            sql.set_blacklist_strength(chat_id, 1, "0")
        elif args[0].lower() == "warn":
            settypeblacklist = "warned"
            sql.set_blacklist_strength(chat_id, 2, "0")
        elif args[0].lower() == "mute":
            settypeblacklist = "muted"
            sql.set_blacklist_strength(chat_id, 3, "0")
        elif args[0].lower() == "kick":
            settypeblacklist = "kicked"
            sql.set_blacklist_strength(chat_id, 4, "0")
        elif args[0].lower() == "ban":
            settypeblacklist = "banned"
            sql.set_blacklist_strength(chat_id, 5, "0")
        elif args[0].lower() == "tban":
            if len(args) == 1:
                teks = """It looks like you are trying to set a temporary value to blacklist, but has not determined the time; use `/blstickermode tban <timevalue>`.
                                              Examples of time values: 4m = 4 minute, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
                send_message(update.effective_message, teks, parse_mode="markdown")
                return
            settypeblacklist = "temporary banned for {}".format(args[1])
            sql.set_blacklist_strength(chat_id, 6, str(args[1]))
        elif args[0].lower() == "tmute":
            if len(args) == 1:
                teks = """It looks like you are trying to set a temporary value to blacklist, but has not determined the time; use `/blstickermode tmute <timevalue>`.
                                              Examples of time values: 4m = 4 minute, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
                send_message(update.effective_message, teks, parse_mode="markdown")
                return
            settypeblacklist = "temporary muted for {}".format(args[1])
            sql.set_blacklist_strength(chat_id, 7, str(args[1]))
        else:
            send_message(
                update.effective_message,
                "I ᴄᴀɴ ᴏɴʟʏ ᴜɴᴅᴇʀsᴛᴀɴᴅ off/del/warn/ban/kick/mute/tban/tmute!",
            )
            return
        if conn:
            text = "Bʟᴀᴄᴋʟɪsᴛ sᴛɪᴄᴋᴇʀ ᴍᴏᴅᴇ ᴄʜᴀɴɢᴇᴅ, ᴜsᴇʀs ɴᴏᴡ ᴡɪʟʟ ʙᴇ `{}` ᴀᴛ *{}*!".format(
                settypeblacklist,
                chat_name,
            )
        else:
            text = "Bʟᴀᴄᴋʟɪsᴛ sᴛɪᴄᴋᴇʀ ᴍᴏᴅᴇ ᴄʜᴀɴɢᴇᴅ, ᴜsᴇʀs ᴡɪʟʟ ʙᴇ`{}`!".format(
                settypeblacklist,
            )
        send_message(update.effective_message, text, parse_mode="markdown")
        return (
            "<b>{}:</b>\n"
            "<b>Aᴅᴍɪɴ:</b> {}\n"
            "Cʜᴀɴɢᴇᴅ sᴛɪᴄᴋᴇʀ ʙʟᴀᴄᴋʟɪsᴛ ᴍᴏᴅᴇ. ᴜsᴇʀs ᴡɪʟ ʙᴇ {}.".format(
                html.escape(chat.title),
                mention_html(user.id, html.escape(user.first_name)),
                settypeblacklist,
            )
        )
    getmode, getvalue = sql.get_blacklist_setting(chat.id)
    if getmode == 0:
        settypeblacklist = "not active"
    elif getmode == 1:
        settypeblacklist = "delete"
    elif getmode == 2:
        settypeblacklist = "warn"
    elif getmode == 3:
        settypeblacklist = "mute"
    elif getmode == 4:
        settypeblacklist = "kick"
    elif getmode == 5:
        settypeblacklist = "ban"
    elif getmode == 6:
        settypeblacklist = "temporarily banned for {}".format(getvalue)
    elif getmode == 7:
        settypeblacklist = "temporarily muted for {}".format(getvalue)
    if conn:
        text = "Bʟᴀᴄᴋʟɪsᴛ sᴛɪᴄᴋᴇʀ ᴍᴏᴅᴇ ɪs ᴄᴜʀʀᴇɴᴛʟʏ sᴇᴛ ᴛᴏ *{}* ɪɴ *{}*.".format(
            settypeblacklist,
            chat_name,
        )
    else:
        text = "Bʟᴀᴄᴋʟɪsᴛ sᴛɪᴄᴋᴇʀ ᴍᴏᴅᴇ ɪs ᴄᴜʀʀᴇɴᴛʟʏ sᴇᴛ ᴛᴏ *{}*.".format(
            settypeblacklist,
        )
    send_message(update.effective_message, text, parse_mode=ParseMode.MARKDOWN)
    return ""


@user_not_admin
def del_blackliststicker(update: Update, context: CallbackContext):
    bot = context.bot
    chat = update.effective_chat  # type: Optional[Chat]
    message = update.effective_message  # type: Optional[Message]
    user = update.effective_user
    to_match = message.sticker
    if not to_match or not to_match.set_name:
        return
    bot = context.bot
    getmode, value = sql.get_blacklist_setting(chat.id)

    chat_filters = sql.get_chat_stickers(chat.id)
    for trigger in chat_filters:
        if to_match.set_name.lower() == trigger.lower():
            try:
                if getmode == 0:
                    return
                if getmode == 1:
                    message.delete()
                elif getmode == 2:
                    message.delete()
                    warn(
                        update.effective_user,
                        chat,
                        "Using sticker '{}' which in blacklist stickers".format(
                            trigger,
                        ),
                        message,
                        update.effective_user,
                        # conn=False,
                    )
                    return
                elif getmode == 3:
                    message.delete()
                    bot.restrict_chat_member(
                        chat.id,
                        update.effective_user.id,
                        permissions=ChatPermissions(can_send_messages=False),
                    )
                    bot.sendMessage(
                        chat.id,
                        "{} ᴍᴜᴛᴇᴅ ʙᴀᴄᴀᴜsᴇ ᴜsɪɴɢ '{}' ᴡʜɪᴄʜ ɪs ɪɴ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ sᴛɪᴄᴋᴇʀs".format(
                            mention_markdown(user.id, user.first_name),
                            trigger,
                        ),
                        parse_mode="markdown",
                    )
                    return
                elif getmode == 4:
                    message.delete()
                    res = chat.unban_member(update.effective_user.id)
                    if res:
                        bot.sendMessage(
                            chat.id,
                            "{} ᴋɪᴄᴋᴇᴅ ʙᴀᴄᴀᴜsᴇ ᴜsɪɴɢ '{}' ᴡʜɪᴄʜ ɪs ɪɴ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ sᴛɪᴄᴋᴇʀs".format(
                                mention_markdown(user.id, user.first_name),
                                trigger,
                            ),
                            parse_mode="markdown",
                        )
                    return
                elif getmode == 5:
                    message.delete()
                    chat.kick_member(user.id)
                    bot.sendMessage(
                        chat.id,
                        "{} ʙᴀɴɴᴇᴅ ʙᴇᴄᴀᴜsᴇ ᴜsɪɴɢ '{}' ᴡʜɪᴄʜ ɪs ɪɴ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ sᴛɪᴄᴋᴇʀs".format(
                            mention_markdown(user.id, user.first_name),
                            trigger,
                        ),
                        parse_mode="markdown",
                    )
                    return
                elif getmode == 6:
                    message.delete()
                    bantime = extract_time(message, value)
                    chat.kick_member(user.id, until_date=bantime)
                    bot.sendMessage(
                        chat.id,
                        "{} ʙᴀɴɴᴇᴅ ғᴏʀ {} ʙᴇᴄᴀᴜsᴇ ᴏғ ᴜsɪɴɢ '{}' ᴡʜɪᴄʜ ɪs ɪɴ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ sᴛɪᴄᴋᴇʀs".format(
                            mention_markdown(user.id, user.first_name),
                            value,
                            trigger,
                        ),
                        parse_mode="markdown",
                    )
                    return
                elif getmode == 7:
                    message.delete()
                    mutetime = extract_time(message, value)
                    bot.restrict_chat_member(
                        chat.id,
                        user.id,
                        permissions=ChatPermissions(can_send_messages=False),
                        until_date=mutetime,
                    )
                    bot.sendMessage(
                        chat.id,
                        "{} ᴍᴜᴛᴇᴅ ғᴏʀ {} ʙᴇᴄᴀᴜsᴇ ғᴏʀ ᴜsɪɴɢ '{}' ᴡʜɪᴄʜ ɪs ɪɴ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ sᴛɪᴄᴋᴇʀs ʟɪsᴛ".format(
                            mention_markdown(user.id, user.first_name),
                            value,
                            trigger,
                        ),
                        parse_mode="markdown",
                    )
                    return
            except BadRequest as excp:
                if excp.message != "Message to delete not found":
                    LOGGER.exception("Eʀʀᴏʀ ᴡʜɪʟᴇ ᴅᴇʟᴇᴛɪɴɢ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴍᴇssᴀɢᴇ.")
                break


def __import_data__(chat_id, data):
    # set chat blacklist
    blacklist = data.get("sticker_blacklist", {})
    for trigger in blacklist:
        sql.add_to_stickers(chat_id, trigger)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    blacklisted = sql.num_stickers_chat_filters(chat_id)
    return "Tʜᴇʀᴇ ᴀʀᴇ `{} `ʙʟᴀᴄᴋʟɪsᴛᴇᴅ sᴛɪᴄᴋᴇʀs.".format(blacklisted)


def __stats__():
    return "× {} ʙʟᴀᴄᴋʟɪsᴛᴇᴅ sᴛɪᴄᴋᴇʀs, ᴀᴄʀᴏss {} ᴄʜᴀᴛs.".format(
        sql.num_stickers_filters(),
        sql.num_stickers_filter_chats(),
    )


__help__ = """
Bʟᴀᴄᴋʟɪsᴛ sᴛɪᴄᴋᴇʀ ɪs ᴜsᴇᴅ ᴛᴏ sᴛᴏᴘ ᴄᴇʀᴛᴀɪɴ sᴛɪᴄᴋᴇʀs ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ. Wʜᴇɴᴇᴠᴇʀ ᴛʜᴀᴛ sᴛɪᴄᴋᴇʀ ɪs sᴇɴᴛ,ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ɪᴍᴍᴇᴅɪᴀᴛᴇʟʏ ᴅᴇʟᴇᴛᴇᴅ.
*Nᴏᴛᴇ:* Bʟᴀᴄᴋʟɪsᴛ sᴛɪᴄᴋᴇʀs ᴅᴏ ɴᴏᴛ ᴀғғᴇᴄᴛ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs.
 ❍ /blsticker*:* Tᴏ sᴇᴇ ᴄᴜʀʀᴇɴᴛʟʏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ sᴛɪᴄᴋᴇʀs ʟɪsᴛ.
*Aᴅᴍɪɴs /-:*
 ❍ /addblsticker <sticker link>*:* Aᴅᴅ ᴛʜᴇ sᴛɪᴄᴋᴇʀ ᴛʀɪɢɢᴇʀ ᴛᴏ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ. (Cᴀɴ ʙᴇ ᴀᴅᴅᴇᴅ ᴠɪᴀ ʀᴇᴘʟʏ ᴛᴏ sᴛɪᴄᴋᴇʀ).
 ❍ /unblsticker <sticker link>*:* Rᴇᴍᴏᴠᴇ ᴛʀɪɢɢᴇʀs ғʀᴏᴍ ʙʟᴀᴄᴋʟɪsᴛ, Tʜᴇ sᴀᴍᴇ ɴᴇᴡʟɪɴᴇ ʟᴏɢɪᴄ ᴀᴘᴘʟɪᴇs ʜᴇʀᴇ, Sᴏ ʏᴏᴜ ᴄᴀɴ ᴅᴇʟᴇᴛᴇ ᴍᴜʟᴛɪᴘʟᴇ ᴛʀɪɢɢᴇʀs ᴀᴛ ᴏɴᴄᴇ.
 ❍ /rmblsticker <sticker link>*:* Sᴀᴍᴇ ᴀs ᴀʙᴏᴠᴇ.
 ❍ /blstickermode <ban/tban/mute/tmute>*:* Sᴇᴛs ᴜᴘ ᴀ ᴅᴇғᴀᴜʟᴛ ᴀᴄᴛɪᴏɴ ᴏɴ ᴡʜᴀᴛ ᴛᴏ ᴅᴏ ɪғ ᴜsᴇʀs ᴜsᴇ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ sᴛɪᴄᴋᴇʀs.
Nᴏᴛᴇ:
 ❍ <sticker link> ᴄᴀɴ ʙᴇ `https://t.me/addstickers/<sticker>` ᴏʀ ᴊᴜsᴛ `<sticker>` ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴇ sᴛɪᴄᴋᴇʀ ᴍᴇssᴀɢᴇ.
"""

__mod_name__ = "Bʟ-Sᴛɪᴄᴋ"

BLACKLIST_STICKER_HANDLER = DisableAbleCommandHandler(
    "blsticker",
    blackliststicker,
    admin_ok=True,
    run_async=True,
)
ADDBLACKLIST_STICKER_HANDLER = DisableAbleCommandHandler(
    "addblsticker",
    add_blackliststicker,
    run_async=True,
)
UNBLACKLIST_STICKER_HANDLER = CommandHandler(
    ["unblsticker", "rmblsticker"],
    unblackliststicker,
    run_async=True,
)
BLACKLISTMODE_HANDLER = CommandHandler("blstickermode", blacklist_mode)
BLACKLIST_STICKER_DEL_HANDLER = MessageHandler(
    Filters.sticker & Filters.chat_type.groups,
    del_blackliststicker,
    run_async=True,
)

dispatcher.add_handler(BLACKLIST_STICKER_HANDLER)
dispatcher.add_handler(ADDBLACKLIST_STICKER_HANDLER)
dispatcher.add_handler(UNBLACKLIST_STICKER_HANDLER)
dispatcher.add_handler(BLACKLISTMODE_HANDLER)
dispatcher.add_handler(BLACKLIST_STICKER_DEL_HANDLER)
