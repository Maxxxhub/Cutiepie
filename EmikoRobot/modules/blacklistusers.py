import html
import EmikoRobot.modules.sql.blacklistusers_sql as sql
from EmikoRobot import (
    DEV_USERS,
    OWNER_ID,
    DRAGONS,
    DEMONS,
    TIGERS,
    WOLVES,
    dispatcher,
) 
from EmikoRobot.modules.helper_funcs.chat_status import dev_plus
from EmikoRobot.modules.helper_funcs.extraction import (
    extract_user,
    extract_user_and_text,
)
from EmikoRobot.modules.log_channel import gloggable
from telegram import ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler
from telegram.utils.helpers import mention_html

BLACKLISTWHITELIST = [OWNER_ID] + DEV_USERS + DRAGONS + WOLVES + DEMONS
BLABLEUSERS = [OWNER_ID] + DEV_USERS


@dev_plus
@gloggable
def bl_user(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("I ᴅᴏᴜʙᴛ ᴛʜᴀᴛ's ᴀ ᴜsᴇʀ.")
        return ""

    if user_id == bot.id:
        message.reply_text("Hᴏᴡ ᴀᴍ ɪ sᴜᴘᴘᴏsᴇᴅ ᴛᴏ ᴅᴏ ᴍʏ ᴡᴏʀᴋ ɪғ ɪ ᴀᴍ ɪɢɴᴏʀɪɴɢ ᴍʏsᴇʟғ..ʏᴏᴜ ᴋɪɴᴅᴀ ɴᴏᴏʙ.!?")
        return ""

    if user_id in BLACKLISTWHITELIST:
        message.reply_text("Nᴏ!\nNᴏᴛɪᴄɪɴɢ ᴅɪsᴀsᴛᴇʀs ɪs ᴍʏ ᴊᴏʙ.")
        return ""

    try:
        target_user = bot.get_chat(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("I ᴄᴀɴ'ᴛ sᴇᴇᴍs ᴛᴏ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ.")
            return ""
        raise

    sql.blacklist_user(user_id, reason)
    message.reply_text("I sʜᴀʟʟ ɪɢɴᴏʀᴇ ᴛʜᴇ ᴇxɪsᴛᴇɴᴄᴇ ᴏғ ᴛʜɪs ᴜsᴇʀ!")
    log_message = (
        f"🤡#BLACKLIST🤡\n"
        f"<b>📍Aᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>🥀Usᴇʀ:</b> {mention_html(target_user.id, html.escape(target_user.first_name))}"
    )
    if reason:
        log_message += f"\n<b>📄Rᴇᴀsᴏɴ:</b> {reason}"

    return log_message


@dev_plus
@gloggable
def unbl_user(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)

    if not user_id:
        message.reply_text("I ᴅᴏᴜʙᴛ ᴛʜᴀᴛ's ᴀ ᴜsᴇʀ.")
        return ""

    if user_id == bot.id:
        message.reply_text("I ᴀʟᴡᴀʏs ɴᴏᴛɪᴄᴇ ᴍʏsᴇʟғ.")
        return ""

    try:
        target_user = bot.get_chat(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("I ᴄᴀɴ'ᴛ sᴇᴇᴍs ᴛᴏ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ.")
            return ""
        raise

    if sql.is_user_blacklisted(user_id):

        sql.unblacklist_user(user_id)
        message.reply_text("*notices user*")
        log_message = (
            f"🤡#UNBLACKLIST🤡\n"
            f"<b>📍Aᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>🥀Usᴇʀ:</b> {mention_html(target_user.id, html.escape(target_user.first_name))}"
        )

        return log_message
    message.reply_text("I ᴀᴍ ɴᴏᴛ ɪɢɴᴏʀɪɴɢ ᴛʜᴇᴍ ᴀᴛ ᴀʟʟ ᴛʜᴏᴜɢʜ.!")
    return ""


@dev_plus
def bl_users(update: Update, context: CallbackContext):
    users = []
    bot = context.bot
    for each_user in sql.BLACKLIST_USERS:
        user = bot.get_chat(each_user)
        reason = sql.get_reason(each_user)

        if reason:
            users.append(
                f"• {mention_html(user.id, html.escape(user.first_name))} :- {reason}",
            )
        else:
            users.append(f"• {mention_html(user.id, html.escape(user.first_name))}")

    message = "<b>Bʟᴀᴄᴋʟɪsᴛᴇᴅ ᴜsᴇʀs</b>\n"
    if not users:
        message += "Noone is being ignored as of yet."
    else:
        message += "\n".join(users)

    update.effective_message.reply_text(message, parse_mode=ParseMode.HTML)


def __user_info__(user_id):
    is_blacklisted = sql.is_user_blacklisted(user_id)

    text = "Bʟᴀᴄᴋʟɪsᴛᴇᴅ: <b>{}</b>"
    if user_id in [777000, 1087968824]:
        return ""
    if user_id == dispatcher.bot.id:
        return ""
    if int(user_id) in DRAGONS + TIGERS + WOLVES:
        return ""
    if is_blacklisted:
        text = text.format("Yes")
        reason = sql.get_reason(user_id)
        if reason:
            text += f"\nRᴇᴀsᴏɴ: <code>{reason}</code>"
    else:
        text = text.format("No")

    return text


BL_HANDLER = CommandHandler("ignore", bl_user, run_async=True)
UNBL_HANDLER = CommandHandler("notice", unbl_user, run_async=True)
BLUSERS_HANDLER = CommandHandler("ignoredlist", bl_users, run_async=True)

dispatcher.add_handler(BL_HANDLER)
dispatcher.add_handler(UNBL_HANDLER)
dispatcher.add_handler(BLUSERS_HANDLER)

__mod_name__ = "Blacklisting Users"
__handlers__ = [BL_HANDLER, UNBL_HANDLER, BLUSERS_HANDLER]
