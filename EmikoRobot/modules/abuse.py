import asyncio
import io
import os
import random
import re
import string
import textwrap


from random import randint, uniform
from telegram import TelegramError
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters
from time import sleep


from EmikoRobot import telethn, ubot
from EmikoRobot.events import register
from EmikoRobot.modules.helper_funcs.filters import CustomFilters
from EmikoRobot import LOGGER, OWNER_ID, dispatcher

ABUSE_STRINGS = (
    "Fuck off",
    "Stfu go fuck yourself",
    "Ur mum gey",
    "Ur dad lesbo",
    "You Assfucker",
    "Nigga",
    "Ur granny tranny",
    "you noob",
    "Relax your Rear,ders nothing to fear,The Rape train is finally here",
    "Stfu bc",
    "Stfu and Gtfo U nub",
    "GTFO bsdk",
    "CUnt",
    "Madharchod",
    " Gay is here",
    "Ur dad gey bc ",
)


@register(pattern="^/abuse$")
async def _(event):

    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        replyto = reply.sender_id
    else:
        replyto = event.sender_id
    await telethn.send_message(
        event.chat_id, random.choice(ABUSE_STRINGS), reply_to=replyto
    )

