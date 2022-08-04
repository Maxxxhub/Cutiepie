import os
import subprocess
import sys

from contextlib import suppress
from time import sleep

import EmikoRobot

from EmikoRobot import dispatcher
from EmikoRobot.modules.helper_funcs.chat_status import dev_plus
from telegram import TelegramError, Update
from telegram.error import Unauthorized
from telegram.ext import CallbackContext, CommandHandler


@dev_plus
def allow_groups(update: Update, context: CallbackContext):
    args = context.args
    if not args:
        state = "Lockdown is " + "on" if not EmikoRobot.ALLOW_CHATS else "off"
        update.effective_message.reply_text(f"Cᴜʀʀᴇɴᴛ sᴛᴀᴛᴇ: {state}")
        return
    if args[0].lower() in ["off", "no"]:
        EmikoRobot.ALLOW_CHATS = True
    elif args[0].lower() in ["yes", "on"]:
        EmikoRobot.ALLOW_CHATS = False
    else:
        update.effective_message.reply_text("Fᴏʀᴍᴀᴛ: /lockdown Yes/No ᴏʀ Off/On")
        return
    update.effective_message.reply_text("Yᴜᴘs! Lᴏᴄᴋ ᴠᴀʟᴜᴇ ᴛᴏɢɢʟᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅")


@dev_plus
def leave(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    if args:
        chat_id = str(args[0])
        try:
            bot.leave_chat(int(chat_id))
        except TelegramError:
            update.effective_message.reply_text(
                "Nᴏᴘᴇs, I ᴄᴏᴜʟᴅ ɴᴏᴛ ʟᴇᴀᴠᴇ ᴛʜᴀᴛ ɢʀᴏᴜᴘ(ᴅᴜɴɴᴏ ᴡʜʏ ᴛʜᴏ).",
            )
            return
        with suppress(Unauthorized):
            update.effective_message.reply_text("Yᴜᴘ, I ʟᴇғᴛ ᴛʜᴀᴛ ᴄʜᴀᴛ/ɢʀᴏᴜᴘ ❗")
    else:
        update.effective_message.reply_text("Sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ᴄʜᴀᴛ ID")


@dev_plus
def gitpull(update: Update, context: CallbackContext):
    sent_msg = update.effective_message.reply_text(
        "Pᴜʟʟɪᴍɢ ᴀʟʟ ᴄʜᴀɴɢᴇs ʀᴇᴍᴏᴛᴇʟʏ ᴀɴᴅ ᴀᴛᴛᴇᴍᴘᴛɪɴɢ ᴛᴏ ʀᴇsᴛᴀʀᴛ ʏᴏᴜʀ ᴀᴘᴘʟɪᴄᴀᴛɪᴏɴ...",
    )
    subprocess.Popen("git pull", stdout=subprocess.PIPE, shell=True)

    sent_msg_text = sent_msg.text + "\n\nCʜᴀɴɢᴇs ᴘᴜʟʟᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ...I ɢᴜᴇss.. Rᴇsᴛᴀʀᴛɪɴɢ ɪɴ "

    for i in reversed(range(5)):
        sent_msg.edit_text(sent_msg_text + str(i + 1))
        sleep(1)

    sent_msg.edit_text("Rᴇsᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ 🌀")

    os.system("restart.bat")
    os.execv("start.bat", sys.argv)


@dev_plus
def restart(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        "Sᴛᴀʀᴛɪɴɢ ᴀ ɴᴇᴡ ɪɴsᴛᴀɴᴄᴇ ᴀɴᴅ sʜᴜᴛᴛɪɴɢ ᴅᴏᴡɴ ᴛʜɪs ᴏɴᴇ ✅",
    )

    os.system("restart.bat")
    os.execv("start.bat", sys.argv)


LEAVE_HANDLER = CommandHandler("leave", leave, run_async=True)
GITPULL_HANDLER = CommandHandler("gitpull", gitpull, run_async=True)
RESTART_HANDLER = CommandHandler("reboot", restart, run_async=True)
ALLOWGROUPS_HANDLER = CommandHandler("lockdown", allow_groups, run_async=True)

dispatcher.add_handler(ALLOWGROUPS_HANDLER)
dispatcher.add_handler(LEAVE_HANDLER)
dispatcher.add_handler(GITPULL_HANDLER)
dispatcher.add_handler(RESTART_HANDLER)

__help__ = """
*Note:* ~ONLY DEVELOPER COMMAND~ !
⚚ /leave <chat id> - Oʀᴅᴇʀ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ʟᴇᴀᴠᴇ ᴛʜᴇ ᴘᴀʀᴛɪᴄᴜʟᴀʀ ᴄʜᴀᴛ.
⚚ /gitpull - Uᴘᴅᴀᴛᴇ ʏᴏᴜʀ ʜᴇʀᴏᴋᴜ
⚚ /reboot - Rᴇʙᴏᴏᴛ ᴛʜᴇ ᴀᴘᴘʟɪᴄᴀᴛɪᴏɴ/ᴀᴘᴘ ( ᴡᴏʀᴋs ᴏɴʟʏ ғᴏʀ ʜᴇʀᴏᴋᴜ )
⚚ /lockdown on/off - Iғ ᴛᴏɢғʟᴇᴅ ᴛᴏ ᴏɴ, ʙᴏᴛ ᴡɪʟʟ ʟᴇᴀᴠᴇ ᴀʟʟ ᴄʜᴀᴛs ᴡʜᴇʀᴇ ʙᴏᴛ ɪs ᴀᴅᴅᴇᴅ ɴᴇᴡʟʏ.
"""

__mod_name__ = "Dᴇᴠs"
__handlers__ = [LEAVE_HANDLER, GITPULL_HANDLER, RESTART_HANDLER, ALLOWGROUPS_HANDLER]
