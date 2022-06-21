import html
from typing import Optional
import re

from telegram import Message, Chat, Update, User, ChatPermissions

from EmikoRobot import TIGERS, WOLVES, dispatcher
from EmikoRobot.modules.helper_funcs.chat_status import (
    bot_admin,
    is_user_admin,
    user_admin,
    user_admin_no_reply,
)
from EmikoRobot.modules.log_channel import loggable
from EmikoRobot.modules.sql import antiflood_sql as sql
from telegram.error import BadRequest
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.utils.helpers import mention_html
from EmikoRobot.modules.helper_funcs.string_handling import extract_time
from EmikoRobot.modules.connection import connected
from EmikoRobot.modules.helper_funcs.alternate import send_message
from EmikoRobot.modules.sql.approve_sql import is_approved

FLOOD_GROUP = 3


@loggable
def check_flood(update, context) -> str:
    user = update.effective_user  # type: Optional[User]
    chat = update.effective_chat  # type: Optional[Chat]
    msg = update.effective_message  # type: Optional[Message]
    if not user:  # ignore channels
        return ""

    # ignore admins and whitelists
    if is_user_admin(chat, user.id) or user.id in WOLVES or user.id in TIGERS:
        sql.update_flood(chat.id, None)
        return ""
    # ignore approved users
    if is_approved(chat.id, user.id):
        sql.update_flood(chat.id, None)
        return
    should_ban = sql.update_flood(chat.id, user.id)
    if not should_ban:
        return ""

    try:
        getmode, getvalue = sql.get_flood_setting(chat.id)
        if getmode == 1:
            chat.ban_member(user.id)
            execstrings = "Banned"
            tag = "BANNED"
        elif getmode == 2:
            chat.ban_member(user.id)
            chat.unban_member(user.id)
            execstrings = "Kicked"
            tag = "KICKED"
        elif getmode == 3:
            context.bot.restrict_chat_member(
                chat.id,
                user.id,
                permissions=ChatPermissions(can_send_messages=False),
            )
            execstrings = "Muted"
            tag = "MUTED"
        elif getmode == 4:
            bantime = extract_time(msg, getvalue)
            chat.ban_member(user.id, until_date=bantime)
            execstrings = "Bᴀɴɴᴇᴅ ғᴏʀ {}".format(getvalue)
            tag = "TBAN"
        elif getmode == 5:
            mutetime = extract_time(msg, getvalue)
            context.bot.restrict_chat_member(
                chat.id,
                user.id,
                until_date=mutetime,
                permissions=ChatPermissions(can_send_messages=False),
            )
            execstrings = "Mᴜᴛᴇᴅ ғᴏʀ {}".format(getvalue)
            tag = "TMUTE"
        send_message(
            update.effective_message,
            "Bᴇᴇᴘ ʙᴏᴏᴘ! Bᴏᴏᴘ ʙᴇᴇᴘ!\n{}!".format(execstrings),
        )

        return (
            "<b>{}:</b>"
            "\n#{}"
            "\n<b>Usᴇʀ:</b> {}"
            "\nFʟᴏᴏᴅᴇᴅ ᴛʜᴇ ɢʀᴏᴜᴘ.".format(
                tag,
                html.escape(chat.title),
                mention_html(user.id, html.escape(user.first_name)),
            )
        )

    except BadRequest:
        msg.reply_text(
            "I ᴄᴀɴ'ᴛ ʀᴇsᴛʀɪᴄᴛ ᴘᴇᴏᴘʟᴇ' ʜᴇʀᴇ, ɢɪᴍᴍᴇ ᴘᴇʀᴍɪssɪᴏɴs ғɪʀsᴛ! Uɴᴛɪʟ ᴛʜᴇɴ ɪ'ʟʟ ᴅɪsᴀʙʟᴇ ᴀɴᴛɪ-ғʟᴏᴏᴅ.",
        )
        sql.set_flood(chat.id, 0)
        return (
            "<b>{}:</b>"
            "\n#INFO"
            "\nDᴏɴ'ᴛ ʜᴀʙᴇ ᴇɴᴏᴜɢʜ' ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ʀᴇsᴛʀɪᴄᴛ ᴜsᴇʀ, sᴏ ᴀɴᴛɪ-ғʟᴏᴏᴅ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅɪsᴀʙʟᴇᴅ".format(
                chat.title,
            )
        )


@user_admin_no_reply
@bot_admin
def flood_button(update: Update, context: CallbackContext):
    bot = context.bot
    query = update.callback_query
    user = update.effective_user
    match = re.match(r"unmute_flooder\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat = update.effective_chat.id
        try:
            bot.restrict_chat_member(
                chat,
                int(user_id),
                permissions=ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                ),
            )
            update.effective_message.edit_text(
                f"Uɴᴍᴜᴛᴇᴅ ʙʏ {mention_html(user.id, html.escape(user.first_name))}.",
                parse_mode="HTML",
            )
        except:
            pass


@user_admin
@loggable
def set_flood(update, context) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]
    args = context.args

    conn = connected(context.bot, update, chat, user.id, need_admin=True)
    if conn:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if update.effective_message.chat.type == "private":
            send_message(
                update.effective_message,
                "Tʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴍᴇᴀɴᴛ ᴛᴏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘ ɴᴏᴛ ɪɴ PM",
            )
            return ""
        chat_id = update.effective_chat.id
        chat_name = update.effective_message.chat.title

    if len(args) >= 1:
        val = args[0].lower()
        if val in ["off", "no", "0"]:
            sql.set_flood(chat_id, 0)
            if conn:
                text = message.reply_text(
                    "Aɴᴛɪ-ғʟᴏᴏᴅ ʜᴀs ʙᴇᴇɴ ᴅɪsᴀʙʟᴇᴅ ɪɴ {}.".format(chat_name),
                )
            else:
                text = message.reply_text("Aɴᴛɪ-ғʟᴏᴏᴅ ʜᴀs ʙᴇᴇɴ ᴅɪsᴀʙʟᴇᴅ.")

        elif val.isdigit():
            amount = int(val)
            if amount <= 0:
                sql.set_flood(chat_id, 0)
                if conn:
                    text = message.reply_text(
                        "Aɴᴛɪ-ғʟᴏᴏᴅ ʜᴀs ʙᴇᴇɴ ᴅɪsᴀʙʟᴇᴅ ɪɴ {}.".format(chat_name),
                    )
                else:
                    text = message.reply_text("Aɴᴛɪ-ғʟᴏᴏᴅ ʜᴀs ʙᴇᴇɴ ᴅɪsᴀʙʟᴇᴅ.")
                return (
                    "<b>{}:</b>"
                    "\n#SETFLOOD"
                    "\n<b>Aᴅᴍɪɴ:</b> {}"
                    "\nDɪsᴀʙʟᴇ ᴀᴍᴛɪ-ғʟᴏᴏᴅ.".format(
                        html.escape(chat_name),
                        mention_html(user.id, html.escape(user.first_name)),
                    )
                )

            if amount <= 3:
                send_message(
                    update.effective_message,
                    "Aɴᴛɪ-ғʟᴏᴏᴅ ᴍʏsᴛ ʙᴇ ᴇɪᴛʜᴇʀ 0 (ᴛᴏ ᴅɪsᴀʙʟᴇ ᴜsᴇ 0) ᴏʀ ɴᴜᴍʙᴇʀ ɢʀᴇᴀᴛᴇʀ ᴛʜᴀɴ 3!",
                )
                return ""
            sql.set_flood(chat_id, amount)
            if conn:
                text = message.reply_text(
                    "Aɴᴛɪ-ғʟᴏᴏᴅ ʜᴀs ʙᴇᴇɴ sᴇᴛ ᴛᴏ {} ɪɴ: {}".format(
                        amount,
                        chat_name,
                    ),
                )
            else:
                text = message.reply_text(
                    "Sᴜᴄᴄᴇssғᴜʟʟʏ ᴜᴘᴅᴀᴛᴇᴅ ᴀɴᴛɪ-ғʟᴏᴏᴅ ʟɪᴍɪᴛ ᴛᴏ {}!".format(amount),
                )
            return (
                "<b>{}:</b>"
                "\n#SETFLOOD"
                "\n<b>Aᴅᴍɪɴ:</b> {}"
                "\nSᴇᴛ ᴀɴᴛɪғʟᴏᴏᴅ ᴛᴏ <code>{}</code>.".format(
                    html.escape(chat_name),
                    mention_html(user.id, html.escape(user.first_name)),
                    amount,
                )
            )

        else:
            message.reply_text("Iɴᴠᴀʟɪᴅ ᴀʀɢᴜᴍᴇɴᴛ ᴘʟᴇᴀsᴇ ᴜsᴇ ᴀ ɴᴜᴍʙᴇʀ, 'off' or 'no'")
    else:
        message.reply_text(
            (
                "Usᴇ `/setflood number` ᴛᴏ ᴇᴍᴀʙʟᴇ ᴀɴᴛɪ-ғʟᴏᴏᴅ.\nᴏʀ ᴜsᴇ `/setflood off` ᴛᴏ ᴅɪsᴀʙʟᴇ ᴀɴᴛɪғʟᴏᴏᴅ!."
            ),
            parse_mode="markdown",
        )
    return ""


def flood(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message

    conn = connected(context.bot, update, chat, user.id, need_admin=False)
    if conn:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if update.effective_message.chat.type == "private":
            send_message(
                update.effective_message,
                "Tʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴍᴇᴀɴᴛ ᴏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘ, ɴᴏᴛ ɪɴ PM",
            )
            return
        chat_id = update.effective_chat.id
        chat_name = update.effective_message.chat.title

    limit = sql.get_flood_limit(chat_id)
    if limit == 0:
        if conn:
            text = msg.reply_text(
                "I'ᴍ ɴᴏᴛ ᴇɴғᴏʀᴄɪɴɢ ᴀɴʏ ғʟᴏᴏᴅ ᴄᴏɴᴛʀᴏʟ ɪɴ {}!".format(chat_name),
            )
        else:
            text = msg.reply_text("I'ᴍ ɴᴏᴛ ᴇɴғᴏʀᴄɪɴɢ ᴀɴʏ ғʟᴏᴏᴅ ᴄᴏɴᴛʀᴏʟ ʜᴇʀᴇ!")
    else:
        if conn:
            text = msg.reply_text(
                "I'ᴍ ᴄᴜʀʀᴇɴᴛʟʏ ʀᴇsᴛʀɪᴄᴛɪɴɢ ᴍᴇᴍʙᴇʀs ᴀғᴛᴇʀ {} ᴄᴏɴsᴇᴄᴜᴛɪᴠᴇ ᴍsɢ's ɪɴ' {}.".format(
                    limit,
                    chat_name,
                ),
            )
        else:
            text = msg.reply_text(
                "I'ᴍ ᴄᴜʀʀᴇɴᴛʟʏ ʀᴇsᴛʀɪᴄᴛɪɴɢ ᴍᴇᴍʙᴇʀs ᴀғᴛᴇʀ {} ᴄᴏɴsᴇᴄᴜᴛɪᴠᴇ ᴍsɢ's.".format(
                    limit,
                ),
            )


@user_admin
def set_flood_mode(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]
    args = context.args

    conn = connected(context.bot, update, chat, user.id, need_admin=True)
    if conn:
        chat = dispatcher.bot.getChat(conn)
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if update.effective_message.chat.type == "private":
            send_message(
                update.effective_message,
                "Tʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴍᴇᴀɴᴛ ᴛᴏ ᴜsᴇ ɪɴ ɢʀᴏᴜᴘ, ɴᴏᴛ ɪɴ PM",
            )
            return ""
        chat = update.effective_chat
        chat_id = update.effective_chat.id
        chat_name = update.effective_message.chat.title

    if args:
        if args[0].lower() == "ban":
            settypeflood = "ban"
            sql.set_flood_strength(chat_id, 1, "0")
        elif args[0].lower() == "kick":
            settypeflood = "kick"
            sql.set_flood_strength(chat_id, 2, "0")
        elif args[0].lower() == "mute":
            settypeflood = "mute"
            sql.set_flood_strength(chat_id, 3, "0")
        elif args[0].lower() == "tban":
            if len(args) == 1:
                teks = """It looks like you tried to set time value for antiflood but you didn't specified time; Try, `/setfloodmode tban <timevalue>`.
    Examples of time value: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
                send_message(update.effective_message, teks, parse_mode="markdown")
                return
            settypeflood = "tban for {}".format(args[1])
            sql.set_flood_strength(chat_id, 4, str(args[1]))
        elif args[0].lower() == "tmute":
            if len(args) == 1:
                teks = (
                    update.effective_message,
                    """It looks like you tried to set time value for antiflood but you didn't specified time; Try, `/setfloodmode tmute <timevalue>`.
    Examples of time value: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.""",
                )
                send_message(update.effective_message, teks, parse_mode="markdown")
                return
            settypeflood = "tmute for {}".format(args[1])
            sql.set_flood_strength(chat_id, 5, str(args[1]))
        else:
            send_message(
                update.effective_message,
                "I ᴏɴʟʏ ᴜɴᴅᴇʀsᴛᴀɴᴅ ban/kick/mute/tban/tmute!",
            )
            return
        if conn:
            text = msg.reply_text(
                "Exᴄᴇᴇᴅɪɴɢ ᴄᴏᴍsᴇᴄᴜᴛɪᴠᴇ ғʟᴏᴏᴅ ʟɪᴍɪᴛ ᴡɪʟᴘ ʀᴇsᴜʟᴛ ɪɴ {} ɪɴ {}!".format(
                    settypeflood,
                    chat_name,
                ),
            )
        else:
            text = msg.reply_text(
                "Exᴄᴇᴇᴅɪɴɢ ᴄᴏɴsᴇᴄᴜᴛɪᴠᴇ ғʟᴏᴏᴅ ʟɪᴍɪᴛ ᴡɪʟʟ ʀᴇsᴜʟᴛ ɪɴ {}!".format(
                    settypeflood,
                ),
            )
        return (
            "<b>{}:</b>\n"
            "<b>Aᴅᴍɪɴ:</b> {}\n"
            "Hᴀs ᴄʜᴀɴɢᴇᴅ ᴀɴᴛɪ-ғʟᴏᴏᴅ ᴍᴏᴅᴇ. ᴜsᴇʀ ᴡɪʟʟ {}.".format(
                settypeflood,
                html.escape(chat.title),
                mention_html(user.id, html.escape(user.first_name)),
            )
        )
    getmode, getvalue = sql.get_flood_setting(chat.id)
    if getmode == 1:
        settypeflood = "ban"
    elif getmode == 2:
        settypeflood = "kick"
    elif getmode == 3:
        settypeflood = "mute"
    elif getmode == 4:
        settypeflood = "tban for {}".format(getvalue)
    elif getmode == 5:
        settypeflood = "tmute for {}".format(getvalue)
    if conn:
        text = msg.reply_text(
            "Sᴇɴᴅɪɴɢ ᴍᴏʀ ᴍsɢ's ᴛʜᴀɴ ғʟᴏᴏᴅ ʟɪᴍɪᴛ ᴡɪʟʟ ʀᴇsᴜʟᴛ ɪɴ' {} ɪɴ {}.".format(
                settypeflood,
                chat_name,
            ),
        )
    else:
        text = msg.reply_text(
            "Sᴇɴᴅɪɴɢ ᴍᴏʀᴇ ᴍsɢ's' ᴛʜᴀɴ ғʟᴏᴏᴅ ʟɪᴍɪᴛ ᴡᴏɪʟʟ ʀᴇsᴜʟᴛ ɪɴ {}.".format(
                settypeflood,
            ),
        )
    return ""


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    limit = sql.get_flood_limit(chat_id)
    if limit == 0:
        return "Nᴏᴛ ᴇɴғᴏʀᴄɪɴɢ ғʟᴏᴏᴅ ᴄᴏɴᴛʀᴏʟ."
    return "Aɴᴛɪ-ғʟᴏᴏᴅ ʜss ʙᴇᴇɴ sᴇᴛ ᴛᴏ`{}`.".format(limit)

__mod_name__ = "Anti-Flood"

FLOOD_BAN_HANDLER = MessageHandler(
    Filters.all & ~Filters.status_update & Filters.chat_type.groups,
    check_flood,
    run_async=True,
)
SET_FLOOD_HANDLER = CommandHandler(
    "setflood", set_flood, filters=Filters.chat_type.groups, run_async=True
)
SET_FLOOD_MODE_HANDLER = CommandHandler(
    "setfloodmode",
    set_flood_mode,
    pass_args=True,
    run_async=True,
)  # , filters=Filters.chat_type.group)
FLOOD_QUERY_HANDLER = CallbackQueryHandler(
    flood_button, pattern=r"unmute_flooder", run_async=True
)
FLOOD_HANDLER = CommandHandler(
    "flood", flood, filters=Filters.chat_type.groups, run_async=True
)

dispatcher.add_handler(FLOOD_BAN_HANDLER, FLOOD_GROUP)
dispatcher.add_handler(FLOOD_QUERY_HANDLER)
dispatcher.add_handler(SET_FLOOD_HANDLER)
dispatcher.add_handler(SET_FLOOD_MODE_HANDLER)
dispatcher.add_handler(FLOOD_HANDLER)

__handlers__ = [
    (FLOOD_BAN_HANDLER, FLOOD_GROUP),
    SET_FLOOD_HANDLER,
    FLOOD_HANDLER,
    SET_FLOOD_MODE_HANDLER,
]
