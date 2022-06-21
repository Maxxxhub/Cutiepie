import html

from EmikoRobot import ALLOW_EXCL, CustomCommandHandler, dispatcher
from EmikoRobot.modules.disable import DisableAbleCommandHandler
from EmikoRobot.modules.helper_funcs.chat_status import (
    bot_can_delete,
    connection_status,
    dev_plus,
    user_admin,
)
from EmikoRobot.modules.sql import cleaner_sql as sql
from telegram import ParseMode, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
)

CMD_STARTERS = ("/", "!") if ALLOW_EXCL else "/"
BLUE_TEXT_CLEAN_GROUP = 13
CommandHandlerList = (CommandHandler, CustomCommandHandler, DisableAbleCommandHandler)
command_list = [
    "cleanblue",
    "ignoreblue",
    "unignoreblue",
    "listblue",
    "ungignoreblue",
    "gignoreblue",
    "start",
    "help",
    "settings",
    "donate",
    "stalk",
    "aka",
    "leaderboard",
]

for handler_list in dispatcher.handlers:
    for handler in dispatcher.handlers[handler_list]:
        if any(isinstance(handler, cmd_handler) for cmd_handler in CommandHandlerList):
            command_list += handler.command


def clean_blue_text_must_click(update: Update, context: CallbackContext):
    bot = context.bot
    chat = update.effective_chat
    message = update.effective_message
    if chat.get_member(bot.id).can_delete_messages and sql.is_enabled(chat.id):
        fst_word = message.text.strip().split(None, 1)[0]

        if len(fst_word) > 1 and any(
            fst_word.startswith(start) for start in CMD_STARTERS
        ):

            command = fst_word[1:].split("@")
            chat = update.effective_chat

            ignored = sql.is_command_ignored(chat.id, command[0])
            if ignored:
                return

            if command[0] not in command_list:
                message.delete()


@connection_status
@bot_can_delete
@user_admin
def set_blue_text_must_click(update: Update, context: CallbackContext):
    chat = update.effective_chat
    message = update.effective_message
    bot, args = context.bot, context.args
    if len(args) >= 1:
        val = args[0].lower()
        if val in ("off", "no"):
            sql.set_cleanbt(chat.id, False)
            reply = "Bʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴɪɴɢ ʜᴀs ʙᴇᴇɴ ᴅɪsᴀʙʟᴇᴅ ғᴏʀ <b>{}</b>".format(
                html.escape(chat.title),
            )
            message.reply_text(reply, parse_mode=ParseMode.HTML)

        elif val in ("yes", "on"):
            sql.set_cleanbt(chat.id, True)
            reply = "Bʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴɪɴɢ ʜᴀs ʙᴇᴇɴ ᴇɴᴀʙʟᴇᴅ ғᴏʀ <b>{}</b>".format(
                html.escape(chat.title),
            )
            message.reply_text(reply, parse_mode=ParseMode.HTML)

        else:
            reply = "Iɴᴠᴀʟɪᴅ ᴀʀɢᴜᴍᴇɴᴛ.Aᴄᴄᴇᴘᴛᴇᴅ ᴠᴀʟᴜᴇs ᴀʀᴇ 'yes', 'on', 'no', 'off'"
            message.reply_text(reply)
    else:
        clean_status = sql.is_enabled(chat.id)
        clean_status = "Enabled" if clean_status else "Disabled"
        reply = "Bʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴɪɴɢ ғᴏʀ <b>{}</b> : <b>{}</b>".format(
            html.escape(chat.title),
            clean_status,
        )
        message.reply_text(reply, parse_mode=ParseMode.HTML)


@user_admin
def add_bluetext_ignore(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    if len(args) >= 1:
        val = args[0].lower()
        added = sql.chat_ignore_command(chat.id, val)
        if added:
            reply = "<b>{}</b> ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ʙʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴᴇʀ ɪɢɴᴏʀᴇ ʟɪsᴛ.".format(
                args[0],
            )
        else:
            reply = "Cᴏᴍᴍᴀɴᴅ ɪs ᴀʟʀᴇᴀᴅʏ ɪɢɴᴏʀᴇᴅ."
        message.reply_text(reply, parse_mode=ParseMode.HTML)

    else:
        reply = "Nᴏ ᴄᴏᴍᴍᴀɴᴅ sᴜᴘᴘʟɪᴇᴅ ᴛᴏ ʙᴇ ɪɢɴᴏʀᴇᴅ."
        message.reply_text(reply)


@user_admin
def remove_bluetext_ignore(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    if len(args) >= 1:
        val = args[0].lower()
        removed = sql.chat_unignore_command(chat.id, val)
        if removed:
            reply = (
                "<b>{}</b> ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ʙʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴᴇʀ ɪɢɴᴏʀᴇ ʟɪsᴛ.".format(
                    args[0],
                )
            )
        else:
            reply = "Cᴏᴍᴍᴀɴᴅ ɪsɴ'ᴛ ɪɢɴᴏʀᴇᴅ ᴄᴜʀʀᴇɴᴛʟʏ."
        message.reply_text(reply, parse_mode=ParseMode.HTML)

    else:
        reply = "Nᴏ ᴄᴏᴍᴍᴀɴᴅ sᴜᴘᴘʟɪᴇᴅ ᴛᴏ ʙᴇ ᴜɴɪɢɴᴏʀᴇᴅ."
        message.reply_text(reply)


@user_admin
def add_bluetext_ignore_global(update: Update, context: CallbackContext):
    message = update.effective_message
    args = context.args
    if len(args) >= 1:
        val = args[0].lower()
        added = sql.global_ignore_command(val)
        if added:
            reply = "<b>{}</b> ʜᴀs ʙᴇᴇɴ ғᴅᴅᴇᴅ ᴛᴏ ɢʟᴏʙᴀʟ ʙʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴᴇʀ ɪɢɴᴏʀᴇ ʟɪsᴛ.".format(
                args[0],
            )
        else:
            reply = "Cᴏᴍᴍᴀɴᴅ ɪs ᴀʟʀᴇᴀᴅʏ ɪɢɴᴏʀᴇᴅ."
        message.reply_text(reply, parse_mode=ParseMode.HTML)

    else:
        reply = "Nᴏ ᴄᴏᴍᴍᴀɴᴅ sᴜᴘᴘʟɪᴇᴅ ᴛᴏ ʙᴇ ɪɢɴᴏʀᴇᴅ."
        message.reply_text(reply)


@dev_plus
def remove_bluetext_ignore_global(update: Update, context: CallbackContext):
    message = update.effective_message
    args = context.args
    if len(args) >= 1:
        val = args[0].lower()
        removed = sql.global_unignore_command(val)
        if removed:
            reply = "<b>{}</b> ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ɢʟᴏʙᴀʟ ʙʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴᴇʀ ɪɢɴᴏʀᴇ ʟɪsᴛ.".format(
                args[0],
            )
        else:
            reply = "Cᴏᴍᴍᴀɴᴅ ɪsɴ'ᴛ ɪɢɴᴏʀᴇᴅ ᴄᴜʀʀᴇɴᴛʟʏ."
        message.reply_text(reply, parse_mode=ParseMode.HTML)

    else:
        reply = "Nᴏ ᴄᴏᴍᴍᴀɴᴅ sᴜᴘᴘʟɪᴇᴅ ᴛᴏ unignored."
        message.reply_text(reply)


@dev_plus
def bluetext_ignore_list(update: Update, context: CallbackContext):

    message = update.effective_message
    chat = update.effective_chat

    global_ignored_list, local_ignore_list = sql.get_all_ignored(chat.id)
    text = ""

    if global_ignored_list:
        text = "Tʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴄᴏᴍᴍᴀɴᴅs ᴀʀᴇ ᴄᴜʀʀᴇɴᴛʟʏ ɪɢɴᴏʀᴇᴅ ɢʟᴏʙᴀʟʟʏ ғʀᴏᴍ ʙʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴɪɴɢ :\n"

        for x in global_ignored_list:
            text += f" - <code>{x}</code>\n"

    if local_ignore_list:
        text += "\nTʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴄᴏᴍᴍᴀɴᴅs ᴀʀᴇ ᴄᴜʀʀᴇɴᴛʟʏ ɪɢɴᴏʀᴇᴅ ʟᴏᴄᴀʟʟʏ ғʀᴏᴍ ʙʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴɪɴɢ :\n"

        for x in local_ignore_list:
            text += f" - <code>{x}</code>\n"

    if text == "":
        text = "Nᴏ ᴄᴏᴍᴍᴀɴᴅs ᴀʀᴇ ᴄᴜʀʀᴇᴍᴛʟʏ ɪɢɴᴏʀᴇᴅ ғʀᴏᴍ ʙʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀᴀɴɪɴɢ."
        message.reply_text(text)
        return

    message.reply_text(text, parse_mode=ParseMode.HTML)
    return


__help__ = """
✘ ᗷᒪᑌᗴ Tᗴ᙭T ᑕᒪᗴᗩᑎᗴᖇ ᖇᗴᗰOᐯᗴᗪ ᗩᑎY ᗰᗩᗪᗴ ᑌᑭ ᑕOᗰᗰᗩᑎᗪՏ TᕼᗩT ᑭᖇOᑭᒪᗴ Տᗴᑎᗪ Iᑎ Tᕼᗴ ᑕᕼᗩT ✘.
➻ /cleanblue <on/off/yes/no>*:* Cʟᴇᴀɴ ᴄᴏᴍᴍᴀɴᴅs ᴀғᴛᴇʀ sᴇɴᴅɪɴɢ.
➻ /ignoreblue <word>*:* Pʀᴇᴠᴇɴᴛ ᴀᴜᴛᴏᴄʟᴇᴀɴɪɴɢ ᴏғ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ.
➻ /unignoreblue <word>*:* Rᴇᴍᴏᴠᴇ ᴘʀᴇᴠᴇɴᴛ ᴀᴜᴛᴏᴄʟᴇᴀɴɪɴɢ ᴏғ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ.
➻ /listblue*:* Lɪsᴛ ᴄᴜʀʀᴇɴᴛʟʏ ᴡʜɪᴛᴇʟɪsᴛᴇᴅ ᴄᴏᴍᴍᴀɴᴅs.
 *✘ ᖴOᒪᒪOᗯIᑎᘜ ᗩᖇᗴ ᗪIՏᗩՏTᗴᖇՏ OᑎᒪY ᑕOᗰᗰᗩᑎᗪՏ, ᗩᗪᗰIᑎՏ ᑕᗩᑎᑎOT ᑌՏᗴ TᕼᗴՏᗴ ✘:*
➻ /gignoreblue <word>*:* Gʟᴏʙᴀʟʟʏ ɪɢɴᴏʀᴇ ʙʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴɪɴɢ ᴏғ sᴀᴠᴇᴅ ᴀᴄᴄʀᴏss TEDDY.
➻ /ungignoreblue <word>*:* Rᴇᴍᴏᴠᴇ sᴀɪᴅ ᴄᴏᴍᴍᴀɴᴅ ғʀᴏᴍ ɢʟᴏʙᴀʟ ᴄʟᴇᴀɴɪɴɢ ʟɪsᴛ.
"""

SET_CLEAN_BLUE_TEXT_HANDLER = CommandHandler(
    "cleanblue", set_blue_text_must_click, run_async=True
)
ADD_CLEAN_BLUE_TEXT_HANDLER = CommandHandler(
    "ignoreblue", add_bluetext_ignore, run_async=True
)
REMOVE_CLEAN_BLUE_TEXT_HANDLER = CommandHandler(
    "unignoreblue", remove_bluetext_ignore, run_async=True
)
ADD_CLEAN_BLUE_TEXT_GLOBAL_HANDLER = CommandHandler(
    "gignoreblue",
    add_bluetext_ignore_global,
    run_async=True,
)
REMOVE_CLEAN_BLUE_TEXT_GLOBAL_HANDLER = CommandHandler(
    "ungignoreblue",
    remove_bluetext_ignore_global,
    run_async=True,
)
LIST_CLEAN_BLUE_TEXT_HANDLER = CommandHandler(
    "listblue", bluetext_ignore_list, run_async=True
)
CLEAN_BLUE_TEXT_HANDLER = MessageHandler(
    Filters.command & Filters.chat_type.groups,
    clean_blue_text_must_click,
    run_async=True,
)

dispatcher.add_handler(SET_CLEAN_BLUE_TEXT_HANDLER)
dispatcher.add_handler(ADD_CLEAN_BLUE_TEXT_HANDLER)
dispatcher.add_handler(REMOVE_CLEAN_BLUE_TEXT_HANDLER)
dispatcher.add_handler(ADD_CLEAN_BLUE_TEXT_GLOBAL_HANDLER)
dispatcher.add_handler(REMOVE_CLEAN_BLUE_TEXT_GLOBAL_HANDLER)
dispatcher.add_handler(LIST_CLEAN_BLUE_TEXT_HANDLER)
dispatcher.add_handler(CLEAN_BLUE_TEXT_HANDLER, BLUE_TEXT_CLEAN_GROUP)

__mod_name__ = "Cʟᴇᴀɴᴇʀ"
__handlers__ = [
    SET_CLEAN_BLUE_TEXT_HANDLER,
    ADD_CLEAN_BLUE_TEXT_HANDLER,
    REMOVE_CLEAN_BLUE_TEXT_HANDLER,
    ADD_CLEAN_BLUE_TEXT_GLOBAL_HANDLER,
    REMOVE_CLEAN_BLUE_TEXT_GLOBAL_HANDLER,
    LIST_CLEAN_BLUE_TEXT_HANDLER,
    (CLEAN_BLUE_TEXT_HANDLER, BLUE_TEXT_CLEAN_GROUP),
]
