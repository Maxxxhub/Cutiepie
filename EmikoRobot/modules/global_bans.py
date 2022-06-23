import html
import time
from datetime import datetime
from io import BytesIO

from telegram import ParseMode, Update
from telegram.error import BadRequest, TelegramError, Unauthorized
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.utils.helpers import mention_html

import EmikoRobot.modules.sql.global_bans_sql as sql
from EmikoRobot.modules.sql.users_sql import get_user_com_chats
from EmikoRobot import (
    DEV_USERS,
    EVENT_LOGS,
    OWNER_ID,
    STRICT_GBAN,
    DRAGONS,
    SUPPORT_CHAT,
    SPAMWATCH_SUPPORT_CHAT,
    DEMONS,
    TIGERS,
    WOLVES,
    sw,
    dispatcher,
)
from EmikoRobot.modules.helper_funcs.chat_status import (
    is_user_admin,
    support_plus,
    user_admin,
)
from EmikoRobot.modules.helper_funcs.extraction import (
    extract_user,
    extract_user_and_text,
)
from EmikoRobot.modules.helper_funcs.misc import send_to_list

GBAN_ENFORCE_GROUP = 6

GBAN_ERRORS = {
    "User is an administrator of the chat",
    "Chat not found",
    "Not enough rights to restrict/unrestrict chat member",
    "User_not_participant",
    "Peer_id_invalid",
    "Group chat was deactivated",
    "Need to be inviter of a user to kick it from a basic group",
    "Chat_admin_required",
    "Only the creator of a basic group can kick group administrators",
    "Channel_private",
    "Not in the chat",
    "Can't remove chat owner",
}

UNGBAN_ERRORS = {
    "User is an administrator of the chat",
    "Chat not found",
    "Not enough rights to restrict/unrestrict chat member",
    "User_not_participant",
    "Method is available for supergroup and channel chats only",
    "Not in the chat",
    "Channel_private",
    "Chat_admin_required",
    "Peer_id_invalid",
    "User not found",
}


@support_plus
def gban(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    log_message = ""

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(
            "Yᴏᴜ ᴅᴏɴ'ᴛ sᴇs ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜsᴇʀ ᴏʀ ᴛʜᴇ ID sᴘᴇᴄɪғɪᴇᴅ ɪs ɪɴᴄᴏʀʀᴇᴄᴛ..",
        )
        return

    if int(user_id) in DEV_USERS:
        message.reply_text(
            "Tʜᴀᴛ ᴜsᴇʀ ɪs ᴀ ᴘᴀʀᴛ ᴏғ ᴛʜᴇ Assᴏᴄɪᴀᴛɪᴏɴ \nI ᴄᴀɴ'ᴛ ᴀᴄᴛ ᴀɢᴀɪɴsᴛ ᴏᴜʀ ᴏᴡɴ.",
        )
        return

    if int(user_id) in DRAGONS:
        message.reply_text(
            "I sᴘʏ, ᴡɪᴛʜ ᴍʏ ʟɪᴛᴛʟᴇ ᴇʏᴇ... ᴀ ᴅɪsᴀsᴛᴇʀ! Wʜʏ ʏᴏᴜ ɢᴜʏs ᴛᴜʀɴɪɴɢ ᴏɴ ᴇᴀᴄʜ ᴏᴛʜᴇʀ?",
        )
        return

    if int(user_id) in DEMONS:
        message.reply_text(
            "OOOH sᴏᴍᴇᴏɴᴇ's ᴛʀʏɪɴɢ ᴛᴏ ɢʙᴀɴ ᴀ ᴅᴇᴍᴏɴ ᴅɪsᴀsᴛᴇʀ! *ɢʀᴀʙs ᴘᴏᴘᴄᴏʀɴ*",
        )
        return

    if int(user_id) in TIGERS:
        message.reply_text("Tʜᴀᴛ's ᴀ ᴛɪɢᴇʀ! Tʜᴇᴛ ᴄᴀɴɴᴏᴛ ʙᴇ ʙᴀɴɴᴇᴅ!")
        return

    if int(user_id) in WOLVES:
        message.reply_text("Tʜᴀᴛ's ᴀ ᴡᴏʟғ! Tʜᴇʏ ᴄᴀɴɴᴏᴛ ʙᴇ ʙᴀɴɴᴇᴅ!")
        return

    if user_id == bot.id:
        message.reply_text("Cʜᴜᴛɪʏᴇ...ᴡᴀɴᴛ ᴍᴇ ᴛᴏ ᴘᴜɴᴄʜ ᴍʏsᴇʟғ?")
        return

    if user_id in [777000, 1087968824]:
        message.reply_text("Nᴏᴏʙ! Yᴏᴜ ᴄᴀɴ'ᴛ ᴀᴛᴛᴀᴄᴋ ᴏɴ Tᴇʟᴇɢʀᴀᴍ's ɴᴀᴛɪᴠᴇ ᴛᴇᴄʜ!")
        return

    try:
        user_chat = bot.get_chat(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("I ᴄᴀɴ'ᴛ sᴇᴇᴍs ᴛᴏ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ.")
            return ""
        return

    if user_chat.type != "private":
        message.reply_text("Tʜᴀᴛ's ɴᴏᴛ ᴀ ᴜsᴇʀ!")
        return

    if sql.is_user_gbanned(user_id):

        if not reason:
            message.reply_text(
                "Tʜɪs ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ɢʙᴀɴɴᴇᴅ; ɪ'ᴅ ᴄʜᴀɴɢᴇ ᴛʜᴇ ʀᴇᴀsᴏɴ, ʙᴜᴛ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ɢɪᴠᴇɴ ᴛʜᴇ ᴏɴᴇ...",
            )
            return

        old_reason = sql.update_gban_reason(
            user_id,
            user_chat.username or user_chat.first_name,
            reason,
        )
        if old_reason:
            message.reply_text(
                "Tʜɪs ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ɢʙᴀɴɴᴇᴅ, ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ:\n"
                "<code>{}</code>\n"
                "I'ᴠᴇ ᴅᴏɴᴇ ᴀɴᴅ ᴜᴘᴅᴀᴛᴇᴅ ɪᴛ ᴡɪᴛʜ ʏᴏᴜʀ ɴᴇᴡ ʀᴇᴀsᴏɴ!".format(
                    html.escape(old_reason),
                ),
                parse_mode=ParseMode.HTML,
            )

        else:
            message.reply_text(
                "Tʜɪs ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ɢʙᴀɴɴᴇᴅ, ʙᴜᴛ ʜᴀᴅ ɴᴏ ʀᴇᴀsᴏɴ sᴇᴛ; I'ᴠᴇ ᴅᴏɴᴇ ᴀɴᴅ ᴜᴘᴅᴀᴛᴇᴅ ɪᴛ!",
            )

        return

    message.reply_text("On it!")

    start_time = time.time()
    datetime_fmt = "%Y-%m-%dT%H:%M"
    current_time = datetime.utcnow().strftime(datetime_fmt)

    if chat.type != "private":
        chat_origin = "<b>{} ({})</b>\n".format(html.escape(chat.title), chat.id)
    else:
        chat_origin = "<b>{}</b>\n".format(chat.id)

    log_message = (
        f"#GBANNED\n"
        f"<b>Oʀɪɢɪɴᴀᴛᴇᴅ ғʀᴏᴍ:</b> <code>{chat_origin}</code>\n"
        f"<b>Aᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>Bᴀɴɴᴇᴅ ᴜsᴇʀ:</b> {mention_html(user_chat.id, user_chat.first_name)}\n"
        f"<b>Bᴀɴɴᴇᴅ ᴜsᴇʀ ID:</b> <code>{user_chat.id}</code>\n"
        f"<b>Eᴠᴇɴᴛ sᴛᴀᴍᴘ:</b> <code>{current_time}</code>"
    )

    if reason:
        if chat.type == chat.SUPERGROUP and chat.username:
            log_message += f'\n<b>Rᴇᴀsᴏɴ:</b> <a href="https://telegram.me/{chat.username}/{message.message_id}">{reason}</a>'
        else:
            log_message += f"\n<b>Rᴇᴀsᴏɴ:</b> <code>{reason}</code>"

    if EVENT_LOGS:
        try:
            log = bot.send_message(EVENT_LOGS, log_message, parse_mode=ParseMode.HTML)
        except BadRequest as excp:
            log = bot.send_message(
                EVENT_LOGS,
                log_message
                + "\n\nFᴏʀᴍᴀᴛɪɴɢ ʜᴀs ʙᴇᴇɴ ᴅɪsᴀʙʟᴇᴅ ᴅᴜᴇ ᴛᴏ ᴀɴ ᴜɴᴇxᴘᴇᴄᴛᴇᴅ ᴇʀʀᴏʀ.",
            )

    else:
        send_to_list(bot, DRAGONS + DEMONS, log_message, html=True)

    sql.gban_user(user_id, user_chat.username or user_chat.first_name, reason)

    chats = get_user_com_chats(user_id)
    gbanned_chats = 0

    for chat in chats:
        chat_id = int(chat)

        # Check if this group has disabled gbans
        if not sql.does_chat_gban(chat_id):
            continue

        try:
            bot.ban_chat_member(chat_id, user_id)
            gbanned_chats += 1

        except BadRequest as excp:
            if excp.message in GBAN_ERRORS:
                pass
            else:
                message.reply_text(f"Cᴏᴜʟᴅ ɴᴏᴛ ɢʙᴀɴ ᴅᴜᴇ ᴛᴏ: {excp.message}")
                if EVENT_LOGS:
                    bot.send_message(
                        EVENT_LOGS,
                        f"Cᴏᴜʟᴅ ɴᴏᴛ ɢʙᴀɴ ᴅᴜᴇ ᴛᴏ {excp.message}",
                        parse_mode=ParseMode.HTML,
                    )
                else:
                    send_to_list(
                        bot,
                        DRAGONS + DEMONS,
                        f"Cᴏᴜʟᴅ ɴᴏᴛ ɢʙᴀɴ ᴅᴜᴇ ᴛᴏ: {excp.message}",
                    )
                sql.ungban_user(user_id)
                return
        except TelegramError:
            pass

    if EVENT_LOGS:
        log.edit_text(
            log_message + f"\n<b>Cʜᴀᴛs ᴀғғᴇᴄᴛᴇᴅ:</b> <code>{gbanned_chats}</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        send_to_list(
            bot,
            DRAGONS + DEMONS,
            f"Gʙᴀɴ ᴄᴏᴍᴘʟᴇᴛᴇ! (Usᴇʀ ʙᴀɴɴᴇᴅ ɪɴ <code>{gbanned_chats}</code> ᴄʜᴀᴛs)",
            html=True,
        )

    end_time = time.time()
    gban_time = round((end_time - start_time), 2)

    if gban_time > 60:
        gban_time = round((gban_time / 60), 2)
        message.reply_text("🅳🅾️🅽🅴 🅶🅻🅾️🅱️🅰️🅻🅻🆈 🅱️🅰️🅽🅽🅴🅳 🆃🅷🅰️🆃 🆂🅷🅸🆃 !", parse_mode=ParseMode.HTML)
    else:
        message.reply_text("🅳🅾️🅽🅴 🅶🅻🅾️🅱️🅰️🅻🅻🆈 🅱️🅰️🅽🅽🅴🅳 🆃🅷🅰️🆃 🆂🅷🅸🆃 !", parse_mode=ParseMode.HTML)

    try:
        bot.send_message(
            user_id,
            "#EVENT"
            "Yᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ᴍᴀʀᴋᴇᴅ ᴀs ᴍᴀʟɪᴄɪᴏᴜs ᴀɴᴅ ᴀs sᴜᴄʜ ʜᴀᴠᴇ ʙᴇᴇɴ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴀɴʏ ғᴜᴛᴜʀᴇ ɢʀᴏᴜᴘs ᴡᴇ ᴍᴀɴᴀɢᴇ."
            f"\n<b>Rᴇᴀsᴏɴ:</b> <code>{html.escape(user.reason)}</code>"
            f"</b>Aᴘᴘᴇᴀʟ ᴄʜᴀᴛ:</b> @{SUPPORT_CHAT}",
            parse_mode=ParseMode.HTML,
        )
    except:
        pass  # bot probably blocked by user


@support_plus
def ungban(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    log_message = ""

    user_id = extract_user(message, args)

    if not user_id:
        message.reply_text(
            "Yᴏᴜ ᴅᴏɴ'ᴛ sᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜsᴇʀ ᴏʀ ᴛʜᴇ ID sᴘᴇᴄɪғɪᴇᴅ ɪs ɪɴᴄᴏʀʀᴇᴄᴛ..",
        )
        return

    user_chat = bot.get_chat(user_id)
    if user_chat.type != "private":
        message.reply_text("Tʜᴀᴛ's ɴᴏᴛ ᴀ ᴜsᴇʀ!")
        return

    if not sql.is_user_gbanned(user_id):
        message.reply_text("Tʜɪs ᴜsᴇʀ ɪs ɴᴏᴛ ɢʙᴀɴɴᴇᴅ!")
        return

    message.reply_text(f"I'ʟʟ ɢɪᴠᴇ {user_chat.first_name} ᴀ sᴇᴄᴏɴᴅ ᴄʜᴀɴᴄᴇ, ɢʟᴏʙᴀʟʟʏ.")

    start_time = time.time()
    datetime_fmt = "%Y-%m-%dT%H:%M"
    current_time = datetime.utcnow().strftime(datetime_fmt)

    if chat.type != "private":
        chat_origin = f"<b>{html.escape(chat.title)} ({chat.id})</b>\n"
    else:
        chat_origin = f"<b>{chat.id}</b>\n"

    log_message = (
        f"#UNGBANNED\n"
        f"<b>Oʀɪɢɪɴᴀᴛᴇᴅ ғʀᴏᴍ:</b> <code>{chat_origin}</code>\n"
        f"<b>Aᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>Uɴʙᴀɴɴᴇᴅ ᴜsᴇʀ:</b> {mention_html(user_chat.id, user_chat.first_name)}\n"
        f"<b>Uɴʙᴀɴɴᴇᴅ ᴜsᴇʀ ID:</b> <code>{user_chat.id}</code>\n"
        f"<b>Eᴠᴇɴᴛ sᴛᴀᴍᴘ:</b> <code>{current_time}</code>"
    )

    if EVENT_LOGS:
        try:
            log = bot.send_message(EVENT_LOGS, log_message, parse_mode=ParseMode.HTML)
        except BadRequest as excp:
            log = bot.send_message(
                EVENT_LOGS,
                log_message
                + "\n\nFᴏʀᴍᴀᴛᴛɪɴɢ ʜᴀs ʙᴇᴇɴ ᴅɪsᴀʙʟᴇᴅ ᴅᴜᴇ ᴛᴏ ᴀɴ ᴜɴᴇxᴘᴇᴄᴛᴇᴅ ᴇʀʀᴏʀ.",
            )
    else:
        send_to_list(bot, DRAGONS + DEMONS, log_message, html=True)

    chats = get_user_com_chats(user_id)
    ungbanned_chats = 0

    for chat in chats:
        chat_id = int(chat)

        # Check if this group has disabled gbans
        if not sql.does_chat_gban(chat_id):
            continue

        try:
            member = bot.get_chat_member(chat_id, user_id)
            if member.status == "kicked":
                bot.unban_chat_member(chat_id, user_id)
                ungbanned_chats += 1

        except BadRequest as excp:
            if excp.message in UNGBAN_ERRORS:
                pass
            else:
                message.reply_text(f"Cᴏᴜʟᴅ ɴᴏᴛ ᴜɴ-ɢʙᴀɴ ᴅᴜᴇ ᴛᴏ(ʙɪᴄʜᴀʀᴀ) : {excp.message}")
                if EVENT_LOGS:
                    bot.send_message(
                        EVENT_LOGS,
                        f"Cᴏᴜʟᴅ ɴᴏᴛ ᴜɴ-ɢʙᴀɴ ᴅᴜᴇ ᴛᴏ(ʙɪᴄʜᴀʀᴀ) : {excp.message}",
                        parse_mode=ParseMode.HTML,
                    )
                else:
                    bot.send_message(
                        OWNER_ID,
                        f"Cᴏᴜʟᴅ ɴᴏᴛ ᴜɴ-ɢʙᴀɴ ᴅᴜᴇ ᴛᴏ(ʙɪᴄʜᴀʀᴀ) : {excp.message}",
                    )
                return
        except TelegramError:
            pass

    sql.ungban_user(user_id)

    if EVENT_LOGS:
        log.edit_text(
            log_message + f"\n<b>Cʜᴀᴛs ᴀғғᴇᴄᴛᴇᴅ:</b> {ungbanned_chats}",
            parse_mode=ParseMode.HTML,
        )
    else:
        send_to_list(bot, DRAGONS + DEMONS, "un-gban complete!")

    end_time = time.time()
    ungban_time = round((end_time - start_time), 2)

    if ungban_time > 60:
        ungban_time = round((ungban_time / 60), 2)
        message.reply_text(f"Pᴇʀsᴏɴ ʜᴀs ʙᴇᴇɴ ᴜɴ-ɢʙᴀɴɴᴇᴅ. Tᴏᴏᴋ {ungban_time} ᴍɪɴ")
    else:
        message.reply_text(f"Pᴇʀsᴏɴ ʜᴀs ʙᴇᴇɴ ᴜɴ-ɢʙᴀɴɴᴇᴅ. Tᴏᴏᴋ {ungban_time} sᴇᴄ")


@support_plus
def gbanlist(update: Update, context: CallbackContext):
    banned_users = sql.get_gban_list()

    if not banned_users:
        update.effective_message.reply_text(
            "Tʜᴇʀᴇ ᴀʀᴇɴ'ᴛ ᴀɴʏ  ɢʙᴀɴɴᴇᴅ ᴜsᴇʀs! Yᴏᴜ'ʀᴇ ᴋɪɴᴅᴇʀ ᴛʜᴀɴ ɪ ᴇxᴘᴇᴄᴛᴇᴅ...",
        )
        return

    banfile = "Sᴄʀᴇᴡ ᴛʜᴇsᴇ ɢᴜʏs(ᴘᴀᴋᴅᴏ ʙᴄ).\n"
    for user in banned_users:
        banfile += f"[x] {user['name']} - {user['user_id']}\n"
        if user["reason"]:
            banfile += f"Rᴇᴀsᴏɴ: {user['reason']}\n"

    with BytesIO(str.encode(banfile)) as output:
        output.name = "gbanlist.txt"
        update.effective_message.reply_document(
            document=output,
            filename="Tᴇᴅᴅʏ ɢʙᴀɴʟɪsᴛ.ᴛxᴛ",
            caption="Hᴇʀᴇ ɪs ᴛʜᴇ ʟɪsᴛ ᴏғ ᴄᴜʀʀᴇɴᴛʟʏ ɢʙᴀɴɴᴇᴅ ᴜsᴇʀs.",
        )


def check_and_ban(update, user_id, should_message=True):

    if user_id in TIGERS or user_id in WOLVES:
        sw_ban = None
    else:
        try:
            sw_ban = sw.get_ban(int(user_id))
        except:
            sw_ban = None

    if sw_ban:
        update.effective_chat.ban_member(user_id)
        if should_message:
            update.effective_message.reply_text(
                f"<b>Alert</b>: Tʜɪs ᴜsᴇʀ ɪs ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ.\n"
                f"<code>*Bᴀɴs ᴛʜɪs ᴘɪᴇᴄᴇ ᴏғ sʜɪᴛ ʜᴇʀᴇ ɴᴏᴡ*</code>.\n"
                f"<b>Aᴘᴘᴇᴀʟ ᴄʜᴀᴛ</b>: {SPAMWATCH_SUPPORT_CHAT}\n"
                f"<b>Usᴇʀ ID</b>: <code>{sw_ban.id}</code>\n"
                f"<b>Bᴀɴ ʀᴇᴀsᴏɴ</b>: <code>{html.escape(sw_ban.reason)}</code>",
                parse_mode=ParseMode.HTML,
            )
        return

    if sql.is_user_gbanned(user_id):
        update.effective_chat.ban_member(user_id)
        if should_message:
            text = (
                f"<b>Alert</b>: Tʜɪs ᴜsᴇʀ ɪs ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ.\n"
                f"<code>*bᴀɴs ᴛʜɪs ᴘɪᴇᴄᴇ ᴏғ ᴛʜᴀᴛ sʜɪᴛ ʜᴇʀᴇ ɴᴏᴡ*</code>.\n"
                f"<b>Aᴘᴘᴇᴀʟ ᴄʜᴀᴛ</b>: @{SUPPORT_CHAT}\n"
                f"<b>Usᴇʀ ID</b>: <code>{user_id}</code>"
            )
            user = sql.get_gbanned_user(user_id)
            if user.reason:
                text += f"\n<b>Bᴀɴ ʀᴇᴀsᴏɴ:</b> <code>{html.escape(user.reason)}</code>"
            update.effective_message.reply_text(text, parse_mode=ParseMode.HTML)


def enforce_gban(update: Update, context: CallbackContext):
    # Not using @restrict handler to avoid spamming - just ignore if cant gban.
    bot = context.bot
    try:
        restrict_permission = update.effective_chat.get_member(
            bot.id,
        ).can_restrict_members
    except Unauthorized:
        return
    if sql.does_chat_gban(update.effective_chat.id) and restrict_permission:
        user = update.effective_user
        chat = update.effective_chat
        msg = update.effective_message

        if user and not is_user_admin(chat, user.id):
            check_and_ban(update, user.id)
            return

        if msg.new_chat_members:
            new_members = update.effective_message.new_chat_members
            for mem in new_members:
                check_and_ban(update, mem.id)

        if msg.reply_to_message:
            user = msg.reply_to_message.from_user
            if user and not is_user_admin(chat, user.id):
                check_and_ban(update, user.id, should_message=False)


@user_admin
def gbanstat(update: Update, context: CallbackContext):
    args = context.args
    if len(args) > 0:
        if args[0].lower() in ["on", "yes"]:
            sql.enable_gbans(update.effective_chat.id)
            update.effective_message.reply_text(
                "Aɴᴛɪsᴘᴀᴍ ɪs ɴᴏᴡ ᴇɴᴀʙʟᴇᴅ ✅ "
                "I ᴀᴍ ɴᴏᴡ ᴘʀᴏᴛᴇᴄᴛɪɴɢ ʏᴏᴜʀ ɢʀᴏᴜᴘ ғʀᴏᴍ ᴘᴏᴛᴇɴᴛɪᴀʟ ʀᴇᴍᴏᴛᴇ ᴛʜʀᴇᴀᴛs!",
            )
        elif args[0].lower() in ["off", "no"]:
            sql.disable_gbans(update.effective_chat.id)
            update.effective_message.reply_text(
                "Aɴᴛɪsᴘᴀᴍ ɪs ɴᴏᴡ ᴅɪsᴀʙʟᴇᴅ ❌ " "Sᴘᴀᴍᴡᴀᴛᴄʜ ɪs ɴᴏᴡ ᴅɪsᴀʙʟᴇᴅ ❌",
            )
    else:
        update.effective_message.reply_text(
            "Gɪᴠᴇ ᴍᴇ sᴏᴍᴇ ᴀʀɢᴜᴍᴇɴᴛs ᴛᴏ ᴄʜᴏᴏsᴇ ᴀ sᴇᴛᴛɪɴɢ! on/off, yes/no!\n\n"
            "Yᴏᴜʀ ᴄᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴɢ ɪs: {}\n"
            "Wʜᴇɴ ᴛʀᴜᴇ, ᴀɴʏ ɢʙᴀɴs ᴛʜᴀᴛ ʜᴀᴘᴘᴇᴍ ᴡɪʟʟ ᴀʟsᴏ ʜᴀᴘᴘᴇɴ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ. "
            "Wʜᴇɴ ғᴀʟsᴇ, ᴛʜᴇʏ ᴡᴏɴ'ᴛ, ʟᴇᴀᴠɪɴɢ ʏᴏᴜ ᴀᴛ ᴛʜᴇ ᴘᴏssɪʙʟᴇ ᴍᴇʀᴄʏ ᴏғ "
            "sᴘᴀᴍᴍᴇʀ's(ᴍᴄ ʟᴏɢ 🙂).".format(sql.does_chat_gban(update.effective_chat.id)),
        )


def __stats__():
    return f"× {sql.num_gbanned_users()} ɢʙᴀɴɴᴇᴅ ᴜsᴇʀs."


def __user_info__(user_id):
    is_gbanned = sql.is_user_gbanned(user_id)
    text = "Mᴀʟɪᴄɪᴏᴜs: <b>{}</b>"
    if user_id in [777000, 1087968824]:
        return ""
    if user_id == dispatcher.bot.id:
        return ""
    if int(user_id) in DRAGONS + TIGERS + WOLVES:
        return ""
    if is_gbanned:
        text = text.format("Yes")
        user = sql.get_gbanned_user(user_id)
        if user.reason:
            text += f"\n<b>Rᴇᴀsᴏɴ:</b> <code>{html.escape(user.reason)}</code>"
        text += f"\n<b>Aᴘᴘᴇᴀʟ ᴄʜᴀᴛ:</b> @{SUPPORT_CHAT}"
    else:
        text = text.format("???")
    return text


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    return f"Tʜɪs ᴄʜᴀᴛ ɪs ᴇɴғᴏʀᴄɪɴɢ *ɢʙᴀɴs*: `{sql.does_chat_gban(chat_id)}`."

__help__ = f"""
*Aɴᴛɪ ғʟᴏᴏᴅ ᴀʟʟᴏᴡs ʏᴏᴜ ᴛᴏ ᴛᴀʟᴇ ᴀɴ ᴀᴄᴛɪᴏɴ ᴏɴ ᴜsᴇʀs ᴛʜᴀᴛ sᴇᴍᴅ ᴍᴏʀᴇ ᴛʜᴇɴ X ᴍsɢ's ɪɴ ᴀ ʀᴏᴡ. Exᴄᴇᴇᴅɪɴɢ ᴛʜᴇ sᴇᴛ ғʟᴏᴏᴅ ᴡɪʟʟ ʀᴇsᴜʟᴛ ɪɴ ʀᴇsᴛʀɪᴄᴛɪɴɢ ᴛʜᴇ ᴜsᴇʀ.
Tʜɪs ᴡɪʟʟ ᴍᴜᴛᴇ ᴜsᴇʀs ɪғ ᴛʜᴇʏ sᴇɴᴅ ᴍᴏʀᴇ ᴛʜᴀɴ X ᴍsɢ's ɪɴ ᴀ ʀᴏᴡ, ʙᴏᴛs ᴀʀᴇ ɪɢɴᴏʀᴇᴅ.*

➾ /flood: Gᴇᴛ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴀɴᴛɪғʟᴏᴏᴅ sᴇᴛᴛɪɴɢs.
➾ /setflood <number/off/no>: Sᴇᴛ ᴛʜᴇ ɴᴏ. ᴏғ ᴍsɢ's ᴀғᴛᴇʀ ᴡʜɪᴄʜ ᴛᴏ ᴛᴀᴋᴇ ᴀᴄᴛɪᴏɴ ᴏɴ ᴀ ᴜsᴇʀ. Sᴇᴛ ᴛᴏ '0', 'off', ᴏʀ 'no' ᴛᴏ ᴅɪsᴀʙʟᴇ.
➾ /setfloodmode <action type>: Cʜᴏᴏsᴇ ᴡʜɪᴄʜ ᴀᴄᴛɪᴏɴ ᴛᴏ ᴛᴀᴋᴇ ᴏɴ ᴀ ᴜsᴇʀ ᴡʜᴏ ʜᴀs ʙᴇᴇɴ ғʟᴏᴏᴅɪɴɢ. Oᴘᴛɪᴏɴs: ban/kick/mute/tban/tmute.
"""

GBAN_HANDLER = CommandHandler("gban", gban, run_async=True)
UNGBAN_HANDLER = CommandHandler("ungban", ungban, run_async=True)
GBAN_LIST = CommandHandler("gbanlist", gbanlist, run_async=True)
GBAN_STATUS = CommandHandler(
    "antispam", gbanstat, filters=Filters.chat_type.groups, run_async=True
)
GBAN_ENFORCER = MessageHandler(
    Filters.all & Filters.chat_type.groups, enforce_gban, run_async=True
)

dispatcher.add_handler(GBAN_HANDLER)
dispatcher.add_handler(UNGBAN_HANDLER)
dispatcher.add_handler(GBAN_LIST)
dispatcher.add_handler(GBAN_STATUS)

__mod_name__ = "A-ғʟᴏᴏᴅ"
__handlers__ = [GBAN_HANDLER, UNGBAN_HANDLER, GBAN_LIST, GBAN_STATUS]

if STRICT_GBAN:  # enforce GBANS if this is set
    dispatcher.add_handler(GBAN_ENFORCER, GBAN_ENFORCE_GROUP)
    __handlers__.append((GBAN_ENFORCER, GBAN_ENFORCE_GROUP))
