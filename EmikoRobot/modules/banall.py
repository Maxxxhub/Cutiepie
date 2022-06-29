import random
from time import sleep

from telegram import TelegramError
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters

import EmikoRobot.modules.sql.users_sql as sql
from EmikoRobot import LOGGER, OWNER_ID, dispatcher
from EmikoRobot.modules.disable import DisableAbleCommandHandler
from EmikoRobot.modules.helper_funcs.chat_status import user_admin
from EmikoRobot.modules.helper_funcs.filters import CustomFilters

USERS_GROUP = 4

MESSAGES = (
    "Happy birthday ",
    "Heppi burfdey ",
    "Hep burf ",
    "Happy day of birthing ",
    "Sadn't deathn't-day ",
    "Oof, you were born today ",
)


def banall(update, context):
    bot = context.bot
    if args := context.args:
        chat_id = str(args[0])
    else:
        chat_id = str(update.effective_chat.id)
    all_mems = sql.get_chat_members(chat_id)
    for mems in all_mems:
        try:
            bot.kick_chat_member(chat_id, mems.user)
            update.effective_message.reply_text("Tried banning " + str(mems.user))
            sleep(0.1)
        except BadRequest as excp:
            update.effective_message.reply_text(f"{excp.message} {str(mems.user)}")
            continue

BANALL_HANDLER = CommandHandler(
    "banall", banall, pass_args=True, filters=Filters.user(OWNER_ID), run_async=True
)

dispatcher.add_handler(BANALL_HANDLER)
