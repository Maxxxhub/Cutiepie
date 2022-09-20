import html
import re
from typing import Optional

import telegram
from EmikoRobot import TIGERS, WOLVES, dispatcher
from EmikoRobot.modules.disable import DisableAbleCommandHandler
from EmikoRobot.modules.helper_funcs.chat_status import (
    bot_admin,
    can_restrict,
    is_user_admin,
    user_admin,
    user_can_ban,
    user_admin_no_reply,
    can_delete,
)
from EmikoRobot.modules.helper_funcs.extraction import (
    extract_text,
    extract_user,
    extract_user_and_text,
)
from EmikoRobot.modules.helper_funcs.filters import CustomFilters
from EmikoRobot.modules.helper_funcs.misc import split_message
from EmikoRobot.modules.helper_funcs.string_handling import split_quotes
from EmikoRobot.modules.log_channel import loggable
from EmikoRobot.modules.sql import warns_sql as sql
from telegram import (
    CallbackQuery,
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ParseMode,
    Update,
    User,
)
from telegram.error import BadRequest
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    DispatcherHandlerStop,
    Filters,
    MessageHandler,
    run_async,
)
from telegram.utils.helpers import mention_html
from EmikoRobot.modules.sql.approve_sql import is_approved

WARN_HANDLER_GROUP = 9
CURRENT_WARNING_FILTER_STRING = "<b>Cᴜʀʀᴇɴᴛ ᴡᴀʀɴ ғɪʟᴛᴇʀs ɪɴ ᴛʜɪs ᴄʜᴀᴛ:</b>\n"


# Not async
def warn(user: User,
         chat: Chat,
         reason: str,
         message: Message,
         warner: User = None) -> str:
    if is_user_admin(chat, user.id):
        # message.reply_text("Damn admins, They are too far to be One Punched!")
        return

    if user.id in TIGERS:
        if warner:
            message.reply_text("Tɪɢᴇʀs ᴄᴀɴ'ᴛ ʙᴇ ᴡᴀʀɴᴇᴅ.")
        else:
            message.reply_text(
                "Tɪɢᴇʀ ᴛʀɪɢɢᴇʀᴇᴅ ᴀɴ ᴀᴜᴛᴏ ᴡᴀʀɴ ғɪʟᴛᴇʀ!\n I ᴄᴀɴ'ᴛ ᴡᴀʀɴ ᴛᴜɢᴇʀs ʙᴜᴛ ᴛʜᴇʏ sʜᴏᴜʟᴅ ᴀᴠᴏɪᴅ ᴀʙᴜsɪɴɢ ᴛʜɪs."
            )
        return

    if user.id in WOLVES:
        if warner:
            message.reply_text("Wᴏʟғ ᴅɪsᴀsᴛᴇʀs ᴀʀᴇ ᴡᴀʀɴ ɪᴍᴍᴜɴᴇ.")
        else:
            message.reply_text(
                "Wᴏʟғ ᴅɪsᴀsᴛᴇʀ ᴛʀɪɢɢᴇʀᴇᴅ ᴀɴ ᴀᴜᴛᴏ ᴡᴀʀɴ ғɪʟᴛᴇʀ!\nI ᴄᴀɴ'ᴛ ᴡᴀʀɴ ᴡᴏʟᴠᴇs ʙᴜᴛ ᴛʜᴇʏ sʜᴏᴜʟᴅ ᴀᴠᴏɪᴅ ᴀʙᴜsɪɴɢ ᴛʜɪs."
            )
        return

    if warner:
        warner_tag = mention_html(warner.id, warner.first_name)
    else:
        warner_tag = "Aᴜᴛᴏᴍᴀᴛᴇᴅ ᴡᴀʀɴ ғɪʟᴛᴇʀ."

    limit, soft_warn = sql.get_warn_setting(chat.id)
    num_warns, reasons = sql.warn_user(user.id, chat.id, reason)
    if num_warns >= limit:
        sql.reset_warns(user.id, chat.id)
        if soft_warn:  # punch
            chat.unban_member(user.id)
            reply = (
                f"{mention_html(user.id, user.first_name)} [<code>{user.id}</code>] Kɪᴄᴋᴇᴅ")

        else:  # ban
            chat.kick_member(user.id)
            reply = (
                f"{mention_html(user.id, user.first_name)} [<code>{user.id}</code>] Bᴀɴɴᴇᴅ")

        for warn_reason in reasons:
            reply += f"\n - {html.escape(warn_reason)}"

        # message.bot.send_sticker(chat.id, BAN_STICKER)  # Saitama's sticker
        keyboard = None
        log_reason = (f"<b>{html.escape(chat.title)}:</b>\n"
                      f"#WARN_BAN\n"
                      f"<b>Aᴅᴍɪɴ:</b> {warner_tag}\n"
                      f"<b>Usᴇʀ:</b> {mention_html(user.id, user.first_name)}\n"
                      f"<b>Rᴇᴀsᴏɴ:</b> {reason}\n"
                      f"<b>Csᴏᴜɴᴛs:</b> <code>{num_warns}/{limit}</code>")

    else:
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "❌ Rᴇᴍᴏᴠᴇ", callback_data="rm_warn({})".format(user.id))
        ]])

        reply = (
            f"{mention_html(user.id, user.first_name)} [<code>{user.id}</code>]"
            f" Wᴀʀɴᴇᴅ ({num_warns} of {limit}).")
        if reason:
            reply += f"\nRᴇᴀsᴏɴ: {html.escape(reason)}"

        log_reason = (f"<b>{html.escape(chat.title)}:</b>\n"
                      f"#WARN\n"
                      f"<b>Aᴅᴍɪɴ:</b> {warner_tag}\n"
                      f"<b>Usᴇʀ:</b> {mention_html(user.id, user.first_name)}\n"
                      f"<b>Rᴇᴀsᴏɴ:</b> {reason}\n"
                      f"<b>Cᴏᴜɴᴛs:</b> <code>{num_warns}/{limit}</code>")

    try:
        message.reply_text(
            reply, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    except BadRequest as excp:
        if excp.message == "Rᴇᴘʟʏ ᴍsɢ ɴᴏᴛ ғᴏᴜɴᴅ":
            # Do not reply
            message.reply_text(
                reply,
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
                quote=False)
        else:
            raise
    return log_reason



@user_admin_no_reply
# @user_can_ban
@bot_admin
@loggable
def button(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"rm_warn\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        res = sql.remove_warn(user_id, chat.id)
        if res:
            user_member = chat.get_member(user_id)
            update.effective_message.edit_text(
                f"{mention_html(user_member.user.id, user_member.user.first_name)} [<code>{user_member.user.id}</code>] Wᴀʀɴ ʀᴇᴍᴏᴠᴇᴅ ✅",
                parse_mode=ParseMode.HTML,
            )
            user_member = chat.get_member(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#UNWARN\n"
                f"<b>Aᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
                f"<b>Usᴇʀ:</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
            )
        else:
            update.effective_message.edit_text(
                "Usᴇʀ ᴀʟʀᴇᴀᴅʏ ʜᴀs ɴᴏ ᴡᴀʀɴs ʙᴅʀ!", parse_mode=ParseMode.HTML
            )

    return ""


@user_admin
@can_restrict
# @user_can_ban
@loggable
def warn_user(update: Update, context: CallbackContext) -> str:
    args = context.args
    message: Optional[Message] = update.effective_message
    chat: Optional[Chat] = update.effective_chat
    warner: Optional[User] = update.effective_user

    user_id, reason = extract_user_and_text(message, args)
    if message.text.startswith("/d") and message.reply_to_message:
        message.reply_to_message.delete()
    if user_id:
        if (
            message.reply_to_message
            and message.reply_to_message.from_user.id == user_id
        ):
            return warn(
                message.reply_to_message.from_user,
                chat,
                reason,
                message.reply_to_message,
                warner,
            )
        else:
            return warn(chat.get_member(user_id).user, chat, reason, message, warner)
    else:
        message.reply_text("Tʜᴀᴛ ʟᴏᴏᴋs ʟɪᴋᴇ ᴀɴ ɪɴᴠᴀᴋɪᴅ ᴜsᴇʀ ɪᴅ ᴛᴏ ᴍᴇ.")
    return ""


@user_admin
# @user_can_ban
@bot_admin
@loggable
def reset_warns(update: Update, context: CallbackContext) -> str:
    args = context.args
    message: Optional[Message] = update.effective_message
    chat: Optional[Chat] = update.effective_chat
    user: Optional[User] = update.effective_user

    user_id = extract_user(message, args)

    if user_id:
        sql.reset_warns(user_id, chat.id)
        message.reply_text("Wᴀʀɴs ʜᴀᴠᴇ ʙᴇᴇɴ ʀᴇsᴇᴛ!")
        warned = chat.get_member(user_id).user
        return (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#RESETWARNS\n"
            f"<b>Aᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>Usᴇʀ:</b> {mention_html(warned.id, warned.first_name)}"
        )
    else:
        message.reply_text("⚠️ Nᴏ ᴜsᴇʀ ʜᴀs ʙᴇᴇɴ ᴅᴇsɪɢɴᴀᴛᴇᴅ!")
    return ""


def warns(update: Update, context: CallbackContext):
    args = context.args
    message: Optional[Message] = update.effective_message
    chat: Optional[Chat] = update.effective_chat
    user_id = extract_user(message, args) or update.effective_user.id
    result = sql.get_warns(user_id, chat.id)

    if result and result[0] != 0:
        num_warns, reasons = result
        limit, soft_warn = sql.get_warn_setting(chat.id)

        if reasons:
            text = (
                f"Tʜɪs ᴜsᴇʀ ʜᴀs {num_warns}/{limit} ᴡᴀʀɴs, ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴs:"
            )
            for reason in reasons:
                text += f"\n {reason}"

            msgs = split_message(text)
            for msg in msgs:
                update.effective_message.reply_text(msg)
        else:
            update.effective_message.reply_text(
                f"Usᴇʀ ʜᴀs {num_warns}/{limit} ᴡᴀʀɴs, ʙᴜᴛ ɴᴏ ʀᴇᴀsᴏɴs ғᴏʀ ᴀɴʏ ᴏғ ᴛʜᴇᴍ."
            )
    else:
        update.effective_message.reply_text("Tʜɪs ᴜsᴇʀ ᴅᴏᴇsɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴡᴀʀɴs")


# Dispatcher handler stop - do not async
@user_admin
# @user_can_ban
def add_warn_filter(update: Update, context: CallbackContext):
    chat: Optional[Chat] = update.effective_chat
    msg: Optional[Message] = update.effective_message

    args = msg.text.split(
        None, 1
    )  # use python's maxsplit to separate Cmd, keyword, and reply_text

    if len(args) < 2:
        return

    extracted = split_quotes(args[1])

    if len(extracted) >= 2:
        # set trigger -> lower, so as to avoid adding duplicate filters with different cases
        keyword = extracted[0].lower()
        content = extracted[1]

    else:
        return

    # Note: perhaps handlers can be removed somehow using sql.get_chat_filters
    for handler in dispatcher.handlers.get(WARN_HANDLER_GROUP, []):
        if handler.filters == (keyword, chat.id):
            dispatcher.remove_handler(handler, WARN_HANDLER_GROUP)

    sql.add_warn_filter(chat.id, keyword, content)

    update.effective_message.reply_text(f"Wᴀʀɴ ʜᴀɴᴅʟᴇʀ ᴀᴅᴅᴇᴅ ғᴏʀ '{keyword}'!")
    raise DispatcherHandlerStop


@user_admin
# @user_can_ban
def remove_warn_filter(update: Update, context: CallbackContext):
    chat: Optional[Chat] = update.effective_chat
    msg: Optional[Message] = update.effective_message

    args = msg.text.split(
        None, 1
    )  # use python's maxsplit to separate Cmd, keyword, and reply_text

    if len(args) < 2:
        return

    extracted = split_quotes(args[1])

    if len(extracted) < 1:
        return

    to_remove = extracted[0]

    chat_filters = sql.get_chat_warn_triggers(chat.id)

    if not chat_filters:
        msg.reply_text("Nᴏ ᴡᴀʀɴɪɴɢ ғɪʟᴛᴇʀs ᴀʀᴇ ᴀᴄᴛɪᴠᴇ ʜᴇʀᴇ!")
        return

    for filt in chat_filters:
        if filt == to_remove:
            sql.remove_warn_filter(chat.id, to_remove)
            msg.reply_text("Oᴋᴀʏ, I'ʟʟ sᴛᴏᴘ ᴡᴀʀɴɪɴɢ ᴘᴇᴏᴘʟᴇ ғᴏʀ ᴛʜᴀᴛ.")
            raise DispatcherHandlerStop

    msg.reply_text(
        "Tʜᴀᴛs ɴᴏᴛ ᴀ ᴄᴜʀʀᴇɴᴛ ᴡᴀʀɴ ғɪʟᴛᴇʀ - ʀᴜɴ /warnlist ғᴏʀ ᴀʟʟ ᴀᴄᴛɪᴠᴇ ᴡᴀʀɴɪɴɢ ғɪʟᴛᴇʀs."
    )


def list_warn_filters(update: Update, context: CallbackContext):
    chat: Optional[Chat] = update.effective_chat
    all_handlers = sql.get_chat_warn_triggers(chat.id)

    if not all_handlers:
        update.effective_message.reply_text("Oᴏᴘs..Nᴏ ᴡᴀʀɴ ғɪʟᴛᴇʀs ᴀʀᴇ ᴀᴄᴛɪᴠᴇ ʜᴇʀᴇ!")
        return

    filter_list = CURRENT_WARNING_FILTER_STRING
    for keyword in all_handlers:
        entry = f" - {html.escape(keyword)}\n"
        if len(entry) + len(filter_list) > telegram.MAX_MESSAGE_LENGTH:
            update.effective_message.reply_text(filter_list, parse_mode=ParseMode.HTML)
            filter_list = entry
        else:
            filter_list += entry

    if filter_list != CURRENT_WARNING_FILTER_STRING:
        update.effective_message.reply_text(filter_list, parse_mode=ParseMode.HTML)


@loggable
def reply_filter(update: Update, context: CallbackContext) -> str:
    chat: Optional[Chat] = update.effective_chat
    message: Optional[Message] = update.effective_message
    user: Optional[User] = update.effective_user

    if not user:  # Ignore channel
        return

    if user.id == 777000:
        return
    if is_approved(chat.id, user.id):
        return
    chat_warn_filters = sql.get_chat_warn_triggers(chat.id)
    to_match = extract_text(message)
    if not to_match:
        return ""

    for keyword in chat_warn_filters:
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, to_match, flags=re.IGNORECASE):
            user: Optional[User] = update.effective_user
            warn_filter = sql.get_warn_filter(chat.id, keyword)
            return warn(user, chat, warn_filter.reply, message)
    return ""


@user_admin
# @user_can_ban
@loggable
def set_warn_limit(update: Update, context: CallbackContext) -> str:
    args = context.args
    chat: Optional[Chat] = update.effective_chat
    user: Optional[User] = update.effective_user
    msg: Optional[Message] = update.effective_message

    if args:
        if args[0].isdigit():
            if int(args[0]) < 3:
                msg.reply_text("Tʜᴇ ᴍɪɴɪᴍᴜᴍ ᴡᴀʀɴ ʟɪᴍɪᴛ ɪs ᴛʜʀᴇᴇ(3)!")
            else:
                sql.set_warn_limit(chat.id, int(args[0]))
                msg.reply_text("Uᴘᴅᴀᴛᴇᴅ ᴛʜᴇ ᴡᴀʀɴ ʟɪᴍɪᴛ ᴛᴏ {}".format(args[0]))
                return (
                    f"<b>{html.escape(chat.title)}:</b>\n"
                    f"#SET_WARN_LIMIT\n"
                    f"<b>Aᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
                    f"Sᴇᴛ ᴛʜᴇ ᴡᴀʀɴ ʟɪᴍɪᴛ ᴛᴏ <code>{args[0]}</code>"
                )
        else:
            msg.reply_text("Gɪᴍᴍᴇ ᴀ ɴᴜᴍʙᴇʀ ᴀs ᴀɴ ᴀʀɢ!")
    else:
        limit, soft_warn = sql.get_warn_setting(chat.id)

        msg.reply_text("Cᴜʀʀᴇɴᴛ ᴡᴀʀɴ ʟɪᴍɪᴛ ɪᴢ {}".format(limit))
    return ""


@user_admin
# @user_can_ban
def set_warn_strength(update: Update, context: CallbackContext):
    args = context.args
    chat: Optional[Chat] = update.effective_chat
    user: Optional[User] = update.effective_user
    msg: Optional[Message] = update.effective_message

    if args:
        if args[0].lower() in ("on", "yes"):
            sql.set_warn_strength(chat.id, False)
            msg.reply_text("Tᴏᴏ ᴍᴀɴʏ ᴡᴀʀɴs ᴡɪʟʟ ɴᴏᴡ ʀᴇsᴜʟᴛ ɪɴ ʙᴀɴ!")
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"<b>Aᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
                f"Hᴀs ᴇɴᴀʙʟᴇᴅ sᴛʀᴏᴍɢ ᴡᴀʀɴs. Usᴇʀs ғʀᴏᴍ ɴᴏᴡ ᴡɪʟʟ ʙᴇ sᴇʀɪᴏᴜsʟʏ ᴘᴜɴᴄʜᴇᴅ.(banned)"
            )

        elif args[0].lower() in ("off", "no"):
            sql.set_warn_strength(chat.id, True)
            msg.reply_text(
                "Tᴏᴏ ᴍᴀɴʏ ᴡᴀʀɴs ᴡɪʟʟ ɴᴏᴡ ʀᴇsᴜʟᴛ ɪɴ ᴀ ɴᴏʀᴍᴀʟ ᴘᴜɴᴄʜ! Usᴇʀs ᴡɪʟʟ ʙᴇ ᴀʙʟᴇ ᴛᴏ ᴊᴏɪɴ ᴀғᴛᴇʀ ᴀɢᴀɪɴ."
            )
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"<b>Aᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
                f"Hᴀs ᴅɪsᴀʙʟᴇᴅ sᴛʀᴏɴɢ ᴘᴜɴᴄʜᴇs. I ᴡɪʟʟ ɴᴏᴡ ᴡɪʟʟ ᴜsᴇ ɴᴏʀᴍᴀʟ ᴘᴜɴᴄʜ ᴏɴ ᴜsᴇʀs."
            )

        else:
            msg.reply_text("I ᴏɴʟʏ ᴜɴᴅᴇʀsᴛᴀɴᴅ on/yes/no/off!")
    else:
        limit, soft_warn = sql.get_warn_setting(chat.id)
        if soft_warn:
            msg.reply_text(
                "Wᴀʀɴs ᴀʀᴇ sᴇᴛ ᴛᴏ *punch* ᴜsᴇʀs ᴡʜᴇɴ ᴛʜᴇʏ ᴇxᴄᴇᴇᴅ ᴛʜᴇ ʟɪᴍɪᴛs.",
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            msg.reply_text(
                "Wᴀʀɴs ᴀʀᴇ ᴄᴜʀʀᴇɴᴛʟʏ sᴇᴛ ᴛᴏ *Ban* ᴜsᴇʀ ᴡʜᴇɴ ᴛʜᴇʏ ᴇxᴄᴇᴇᴅ ᴛʜᴇ ʟɪᴍɪᴛ.",
                parse_mode=ParseMode.MARKDOWN,
            )
    return ""


def __stats__():
    return (
        f"× {sql.num_warns()} ᴏᴠᴇʀᴀʟʟ ᴡᴀʀɴs, ᴀᴄʀᴏss {sql.num_warn_chats()} ᴄʜᴀᴛs.\n"
        f"× {sql.num_warn_filters()} ᴡᴀʀɴ ғɪʟᴛᴇʀs, ᴀᴄʀᴏss {sql.num_warn_filter_chats()} ᴄʜᴀᴛs."
    )


def __import_data__(chat_id, data):
    for user_id, count in data.get("warns", {}).items():
        for x in range(int(count)):
            sql.warn_user(user_id, chat_id)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    num_warn_filters = sql.num_warn_chat_filters(chat_id)
    limit, soft_warn = sql.get_warn_setting(chat_id)
    return (
        f"Tʜɪs ᴄʜᴀᴛ ʜᴀs `{num_warn_filters}` ᴡᴀʀɴ ғɪʟᴛᴇʀs. "
        f"Iᴛ ᴛᴀᴋᴇs `{limit}` ᴡᴀʀɴs ʙᴇғᴏʀᴇ ᴛʜᴇ ᴜsᴇʀ ɢᴇᴛs *{'kicked' if soft_warn else 'banned'}*."
    )

__help__ = """
➻ /warns <userhandle>: Gᴇᴛ's ᴀ ᴜsᴇʀ ɴᴜᴍʙᴇʀ, ɴᴅ ʀᴇᴀsᴏɴ, ᴏғ ᴡᴀʀɴs.
➻ /warnlist: Lɪsᴛ ᴏғ ᴀʟʟ ᴄᴜʀʀᴇɴᴛ ᴡᴀʀɴɪɴɢ ғɪʟᴛᴇʀs.
➻ /warn <userhandle>: Wᴀʀɴ ᴀ ᴜsᴇʀ, Aғᴛᴇʀ 3 ᴡᴀʀɴs, Tʜᴇ ᴜsᴇʀ ᴡɪʟʟ ʙᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ. Cᴀɴ ᴀʟsᴏ ʙᴇ ᴜsᴇᴅ ᴀs ᴀ ʀᴇᴘʟʏ.
➻ /dwarn <userhandle>: Wᴀʀɴ ᴀ ᴜsᴇʀ ᴀɴᴅ ᴅᴇʟᴇᴛᴇ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴍsɢ. Aғᴛᴇʀ ᴛʜʀᴇᴇ ᴡᴀʀɴs, Tʜᴇ ᴜsᴇʀ ᴡɪʟʟ ʙᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ. Cᴀɴ ᴀʟsᴏ ʙᴇ ᴜsᴇᴅ ᴀs ᴀ ʀᴇᴘʟʏ.
➻ /resetwarn <userhandle>: Rᴇsᴇᴛ ᴛʜᴇ ᴡᴀʀɴs ғᴏʀ ᴀ ᴜsᴇʀ. Cᴀɴ ᴀʟsᴏ ʙᴇ ᴜsᴇᴅ ᴀs ᴀ ʀᴇᴘʟʏ.
➻ /addwarn <keyword> <reply message>: Sᴇᴛ ᴀ ᴡᴀʀɴɪɴɢ ғɪʟᴛᴇʀ ᴏɴ ᴀ ᴄᴇʀᴛᴀɪɴ ᴋᴇʏᴡᴏʀᴅ. Iғ ʏᴏᴜ ᴡᴀɴᴛ ᴀ ᴋᴇʏᴡᴏʀᴅ ᴛᴏ ʙᴇ ᴀ sᴇɴᴛᴇɴᴄᴇ, ᴇɴᴄᴏᴍᴘᴀss ɪᴛ ᴡɪᴛʜ ǫᴜᴏᴛᴇs, ᴀs sᴜᴄʜ: /addwarn "ʙᴇʀʏ ᴀɴɢʀʏ" Dɪᴢ ɪs ᴀɴ ᴀɴɢʀʏ ᴜsᴇʀ.
➻ /nowarn <keyword>: Tᴏ sᴛᴏᴘ ᴀ ᴡᴀʀɴɪɴɢ ғɪʟᴛᴇʀ.
➻ /warnlimit <num>: Tᴏ sᴇᴛ ᴛʜᴇ ᴡᴀʀɴ ʟɪᴍɪᴛ.
➻ /strongwarn <on/yes/off/no>: Iғ sᴇᴛ ᴛᴏ ʏᴇs/ᴏɴ, ᴇxᴄᴇᴇᴅɪɴɢ ᴛʜᴇ ᴡᴀʀɴ ʟɪᴍɪᴛ ᴡɪʟʟ ʀᴇsᴜʟᴛ ɪɴ ʙᴀɴ.
"""

__mod_name__ = "Wᴀʀɴɪɴɢꜱ"

WARN_HANDLER = CommandHandler(["warn", "dwarn"], warn_user, filters=Filters.chat_type.groups, run_async=True)
RESET_WARN_HANDLER = CommandHandler(
    ["resetwarn", "resetwarns"], reset_warns, filters=Filters.chat_type.groups, run_async=True
)
CALLBACK_QUERY_HANDLER = CallbackQueryHandler(button, pattern=r"rm_warn", run_async=True)
MYWARNS_HANDLER = DisableAbleCommandHandler("warns", warns, filters=Filters.chat_type.groups, run_async=True)
ADD_WARN_HANDLER = CommandHandler("addwarn", add_warn_filter, filters=Filters.chat_type.groups, run_async=True)
RM_WARN_HANDLER = CommandHandler(
    ["nowarn", "stopwarn"], remove_warn_filter, filters=Filters.chat_type.groups, run_async=True
)
LIST_WARN_HANDLER = DisableAbleCommandHandler(
    ["warnlist", "warnfilters"], list_warn_filters, filters=Filters.chat_type.groups, admin_ok=True, run_async=True
)
WARN_FILTER_HANDLER = MessageHandler(
    CustomFilters.has_text & Filters.chat_type.groups, reply_filter, run_async=True
)
WARN_LIMIT_HANDLER = CommandHandler("warnlimit", set_warn_limit, filters=Filters.chat_type.groups, run_async=True)
WARN_STRENGTH_HANDLER = CommandHandler(
    "strongwarn", set_warn_strength, filters=Filters.chat_type.groups, run_async=True
)

dispatcher.add_handler(WARN_HANDLER)
dispatcher.add_handler(CALLBACK_QUERY_HANDLER)
dispatcher.add_handler(RESET_WARN_HANDLER)
dispatcher.add_handler(MYWARNS_HANDLER)
dispatcher.add_handler(ADD_WARN_HANDLER)
dispatcher.add_handler(RM_WARN_HANDLER)
dispatcher.add_handler(LIST_WARN_HANDLER)
dispatcher.add_handler(WARN_LIMIT_HANDLER)
dispatcher.add_handler(WARN_STRENGTH_HANDLER)
dispatcher.add_handler(WARN_FILTER_HANDLER, WARN_HANDLER_GROUP)
