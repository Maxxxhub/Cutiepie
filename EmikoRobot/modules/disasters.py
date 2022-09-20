import html
import json
import os
from typing import Optional

from EmikoRobot import (
    DEV_USERS,
    OWNER_ID,
    DRAGONS,
    SUPPORT_CHAT,
    DEMONS,
    TIGERS,
    WOLVES,
    dispatcher,
)
from EmikoRobot.modules.helper_funcs.chat_status import (
    dev_plus,
    sudo_plus,
    whitelist_plus,
)
from EmikoRobot.modules.helper_funcs.extraction import extract_user
from EmikoRobot.modules.log_channel import gloggable
from telegram import ParseMode, TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler
from telegram.utils.helpers import mention_html

ELEVATED_USERS_FILE = os.path.join(os.getcwd(), "EmikoRobot/elevated_users.json")


def check_user_id(user_id: int, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    if not user_id:
        reply = "That...is a chat! baka ka omae?"

    elif user_id == bot.id:
        reply = "This does not work that way."

    else:
        reply = None
    return reply


# This can serve as a deeplink example.
# disasters =
# """ Text here """

# do not async, not a handler
# def send_disasters(update):
#    update.effective_message.reply_text(
#        disasters, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

### Deep link example ends


@dev_plus
@gloggable
def addsudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        message.reply_text("Tʜɪs ᴍᴇᴍʙᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀ ᴇᴍᴘᴇʀᴏʀ")
        return ""

    if user_id in DEMONS:
        rt += "Sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴀɪsᴇᴅ ᴄᴀᴘᴛᴀɪɴ ᴛᴏ ᴇᴍᴘᴇʀᴏʀ."
        data["supports"].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        rt += "Sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴀɪsᴇᴅ sᴏʟᴅɪᴇʀ ᴛᴏ ᴇᴍᴘᴇʀᴏʀ."
        data["whitelists"].remove(user_id)
        WOLVES.remove(user_id)

    data["sudos"].append(user_id)
    DRAGONS.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt
        + "\nSᴜᴄᴄᴇssғᴜʟʟʏ ʀᴀɪsᴇᴅ {} ᴛᴏ ᴇᴍᴘᴇʀᴏʀ!".format(
            user_member.first_name,
        ),
    )

    log_message = (
        f"#SUDO\n"
        f"<b>Aᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>Usᴇʀ:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@sudo_plus
@gloggable
def addsupport(
    update: Update,
    context: CallbackContext,
) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "Dᴇᴍᴏᴛᴇs ᴛʜɪs ᴇᴍᴘᴇʀᴏʀ ᴛᴏ ᴄᴀᴘᴛᴀɪɴ"
        data["sudos"].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        message.reply_text("Tʜɪs ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴄᴀᴘᴛᴀɪɴ.")
        return ""

    if user_id in WOLVES:
        rt += "Sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴀᴏsᴇᴅ sᴏʟᴅɪᴇʀ ᴛᴏ ᴄᴀᴘᴛᴀɪɴ"
        data["whitelists"].remove(user_id)
        WOLVES.remove(user_id)

    data["supports"].append(user_id)
    DEMONS.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\n{user_member.first_name} ᴡᴀs ᴀᴅᴅᴇᴅ ᴀs ᴀ ᴄᴀᴘᴛᴀɪɴ!",
    )

    log_message = (
        f"#SUPPORT\n"
        f"<b>Aᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>Usᴇʀ:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@sudo_plus
@gloggable
def addwhitelist(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "Tʜɪs ᴍᴇᴍʙᴇʀ ɪs ᴀ ᴇᴍᴘᴇʀᴏʀ, Dᴇᴍᴏᴛɪɴɢ ᴛᴏ sᴏʟᴅɪᴇʀ."
        data["sudos"].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        rt += "Tʜɪs ɪsᴡʀ ɪs ᴀʟʀᴇᴀsʏ ᴀ ᴄᴀᴘᴛᴀɪɴ, Dᴇᴍᴏᴛɪɴɢ ᴛᴏ sᴏʟᴅɪᴇʀ."
        data["supports"].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        message.reply_text("Tʜɪs ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ɪɴ sᴏʟᴅɪᴇʀ.")
        return ""

    data["whitelists"].append(user_id)
    WOLVES.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\nSᴜᴄᴄᴇssғᴜʟʟʏ ʀᴀɪsᴇᴅ {user_member.first_name} ᴛᴏ ʙᴇ ᴀ sᴏʟᴅɪᴇʀ!",
    )

    log_message = (
        f"#WHITELIST\n"
        f"<b>Aᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>Usᴇʀ:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@sudo_plus
@gloggable
def addtiger(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "Tʜɪs ᴜsᴇʀ ɪs ᴀ ᴅʀᴀɢᴏɴ, Dᴇᴍᴏᴛɪɴɢ ᴛᴏ ᴛʀᴀᴅᴇʀ."
        data["sudos"].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        rt += "Tʜɪs ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀ ᴄᴀᴘᴛᴀɪɴ, Dᴇᴍᴏᴛɪɴɢ ᴛᴏ ᴛʀᴀᴅᴇʀ."
        data["supports"].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        rt += "Tʜɪs ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀ sᴏʟɪᴅᴇʀ, Dᴇᴍᴏᴛɪɴɢ ᴛᴏ ᴛʀᴀᴅᴇʀ."
        data["whitelists"].remove(user_id)
        WOLVES.remove(user_id)

    if user_id in TIGERS:
        message.reply_text("Tʜɪs ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅɢ ᴀ ᴛʀᴀᴅᴇʀ.")
        return ""

    data["tigers"].append(user_id)
    TIGERS.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\nSuccessfully give a money to {user_member.first_name} for to be a Trader!",
    )

    log_message = (
        f"#TIGER\n"
        f"<b>Aᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>Usᴇʀ:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@dev_plus
@gloggable
def removesudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        message.reply_text("Rᴇǫᴜᴇsᴛᴇᴅ HA ᴛᴏ ᴅᴇᴍᴏᴛᴇ ᴛʜɪs ᴜsᴇʀ ᴛᴏ ᴄɪᴠɪʟɪᴀɴ")
        DRAGONS.remove(user_id)
        data["sudos"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNSUDO\n"
            f"<b>Aᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>Usᴇʀ:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = "<b>{}:</b>\n".format(html.escape(chat.title)) + log_message

        return log_message
    message.reply_text("Tʜɪs ᴜsᴇʀ ɪs ɴᴏᴛ ᴀ ᴇᴍᴘᴇʀᴏʀ!")
    return ""


@sudo_plus
@gloggable
def removesupport(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DEMONS:
        message.reply_text("Rᴇǫᴜᴇsᴛᴇᴅ HA ᴛᴏ ᴅᴇᴍᴏᴛᴇ ᴛʜɪs ᴜsᴇʀ ᴛᴏ ᴄɪᴠɪʟɪᴀɴ")
        DEMONS.remove(user_id)
        data["supports"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNSUPPORT\n"
            f"<b>Aᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>Usᴇʀ:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    message.reply_text("Tʜɪs ᴜsᴇʀ ɪs ɴᴏᴛ ᴀ ᴄᴀᴘᴛᴀɪɴ!")
    return ""


@sudo_plus
@gloggable
def removewhitelist(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in WOLVES:
        message.reply_text("Dᴇᴍᴏᴛɪɴɢ ᴛᴏ ɴᴏʀᴍᴀʟ ᴜsᴇʀ")
        WOLVES.remove(user_id)
        data["whitelists"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNWHITELIST\n"
            f"<b>Aᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>Usᴇʀ:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    message.reply_text("Tʜɪs ᴜsᴇʀ ɪs ɴᴏᴛ ᴀ sᴏʟᴅɪᴇʀ!")
    return ""


@sudo_plus
@gloggable
def removetiger(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in TIGERS:
        message.reply_text("Dᴇᴍᴏᴛɪɴɢ ᴛᴏ ɴᴏʀᴍᴀʟ ᴜsᴇʀ")
        TIGERS.remove(user_id)
        data["tigers"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNTIGER\n"
            f"<b>Aᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>Usᴇʀ:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    message.reply_text("Tʜɪs ᴜsᴇʀ ɪᴅ ɴᴏᴛ ᴀ ᴛʀᴀᴅᴇʀ!")
    return ""


@whitelist_plus
def whitelistlist(update: Update, context: CallbackContext):
    reply = "<b>Kɴᴏᴡɴ ᴛʜᴇ ᴛʀᴀᴅᴇʀ 🧜:</b>\n"
    m = update.effective_message.reply_text(
        "<code>Gᴀᴛʜᴇʀɪɴɢ ɪɴᴛᴇʟ..</code>",
        parse_mode=ParseMode.HTML,
    )
    bot = context.bot
    for each_user in WOLVES:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)

            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)


@whitelist_plus
def tigerlist(update: Update, context: CallbackContext):
    reply = "<b>Kɴᴏᴡɴ ᴛʜᴇ sᴏʟᴅɪᴇʀ 🧜‍♂:</b>\n"
    m = update.effective_message.reply_text(
        "<code>Gᴀᴛʜᴇʀɪɴɢ ɪɴᴛᴇʟ..</code>",
        parse_mode=ParseMode.HTML,
    )
    bot = context.bot
    for each_user in TIGERS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)


@whitelist_plus
def supportlist(update: Update, context: CallbackContext):
    bot = context.bot
    m = update.effective_message.reply_text(
        "<code>Gᴀᴛʜᴇʀɪɴɢ ɪɴᴛᴇʟ..</code>",
        parse_mode=ParseMode.HTML,
    )
    reply = "<b>Kɴᴏᴡɴ ᴛʜᴇ ᴄᴀᴘᴛᴀɪɴ 🧞:</b>\n"
    for each_user in DEMONS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)


@whitelist_plus
def sudolist(update: Update, context: CallbackContext):
    bot = context.bot
    m = update.effective_message.reply_text(
        "<code>Gᴀᴛʜᴇʀɪɴɢ ɪɴᴛᴇʟ..</code>",
        parse_mode=ParseMode.HTML,
    )
    true_sudo = list(set(DRAGONS) - set(DEV_USERS))
    reply = "<b>Kɴᴏᴡɴ ᴛʜᴇ ᴇᴍᴘᴇʀᴏʀ  🧞‍♀:</b>\n"
    for each_user in true_sudo:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)


@whitelist_plus
def devlist(update: Update, context: CallbackContext):
    bot = context.bot
    m = update.effective_message.reply_text(
        "<code>Gᴀᴛʜᴇʀɪɴɢ ɪɴᴛᴇʟ..</code>",
        parse_mode=ParseMode.HTML,
    )
    true_dev = list(set(DEV_USERS) - {OWNER_ID})
    reply = "<b>Mᴇᴍʙᴇʀ ᴏғ ғᴀᴍɪʟʏ ᴛʜɪs ᴋɪɴɢᴅᴏᴍ 🤴:</b>\n"
    for each_user in true_dev:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)


SUDO_HANDLER = CommandHandler(("addsudo", "addemperor"), addsudo, run_async=True)
SUPPORT_HANDLER = CommandHandler(("addsupport", "addcaptain"), addsupport, run_async=True)
TIGER_HANDLER = CommandHandler(("addsoldier"), addtiger, run_async=True)
WHITELIST_HANDLER = CommandHandler(
    ("addwhitelist", "addtrader"), addwhitelist, run_async=True
)
UNSUDO_HANDLER = CommandHandler(
    ("removesudo", "removeemperor"), removesudo, run_async=True
)
UNSUPPORT_HANDLER = CommandHandler(
    ("removesupport", "removesoldier"), removesupport, run_async=True
)
UNTIGER_HANDLER = CommandHandler(("removetiger"), removetiger, run_async=True)
UNWHITELIST_HANDLER = CommandHandler(
    ("removewhitelist", "removetrader"), removewhitelist, run_async=True
)
WHITELISTLIST_HANDLER = CommandHandler(
    ["whitelistlist", "trader"], whitelistlist, run_async=True
)
TIGERLIST_HANDLER = CommandHandler(["trader"], tigerlist, run_async=True)
SUPPORTLIST_HANDLER = CommandHandler(
    ["supportlist", "captain"], supportlist, run_async=True
)
SUDOLIST_HANDLER = CommandHandler(["sudolist", "emperor"], sudolist, run_async=True)
DEVLIST_HANDLER = CommandHandler(["devlist", "kingdom"], devlist, run_async=True)

dispatcher.add_handler(SUDO_HANDLER)
dispatcher.add_handler(SUPPORT_HANDLER)
dispatcher.add_handler(TIGER_HANDLER)
dispatcher.add_handler(WHITELIST_HANDLER)
dispatcher.add_handler(UNSUDO_HANDLER)
dispatcher.add_handler(UNSUPPORT_HANDLER)
dispatcher.add_handler(UNTIGER_HANDLER)
dispatcher.add_handler(UNWHITELIST_HANDLER)

dispatcher.add_handler(WHITELISTLIST_HANDLER)
dispatcher.add_handler(TIGERLIST_HANDLER)
dispatcher.add_handler(SUPPORTLIST_HANDLER)
dispatcher.add_handler(SUDOLIST_HANDLER)
dispatcher.add_handler(DEVLIST_HANDLER)

__mod_name__ = "Disasters"
__handlers__ = [
    SUDO_HANDLER,
    SUPPORT_HANDLER,
    TIGER_HANDLER,
    WHITELIST_HANDLER,
    UNSUDO_HANDLER,
    UNSUPPORT_HANDLER,
    UNTIGER_HANDLER,
    UNWHITELIST_HANDLER,
    WHITELISTLIST_HANDLER,
    TIGERLIST_HANDLER,
    SUPPORTLIST_HANDLER,
    SUDOLIST_HANDLER,
    DEVLIST_HANDLER,
]
