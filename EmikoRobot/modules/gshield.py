import asyncio
import os
import re
import better_profanity
import emoji
import nude
import requests
from better_profanity import profanity
from google_trans_new import google_translator
from telethon import events
from telethon.tl.types import ChatBannedRights
from EmikoRobot.confing import get_int_key, get_str_key
from EmikoRobot.services.telethonbasics import is_admin
from EmikoRobot.events import register
from pymongo import MongoClient
from EmikoRobot.modules.sql.nsfw_watch_sql import (
    add_nsfwatch,
    get_all_nsfw_enabled_chat,
    is_nsfwatch_indb,
    rmnsfwatch,
)
from EmikoRobot import telethn as tbot, MONGO_DB_URI, BOT_ID

translator = google_translator()
MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

MONGO_DB_URI = get_str_key("MONGO_DB_URI")

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["TeddyRobot"]

async def is_nsfw(event):
    lmao = event
    if not (
        lmao.gif
        or lmao.video
        or lmao.video_note
        or lmao.photo
        or lmao.sticker
        or lmao.media
    ):
        return False
    if lmao.video or lmao.video_note or lmao.sticker or lmao.gif:
        try:
            starkstark = await event.client.download_media(lmao.media, thumb=-1)
        except:
            return False
    elif lmao.photo or lmao.sticker:
        try:
            starkstark = await event.client.download_media(lmao.media)
        except:
            return False
    img = starkstark
    f = {"file": (img, open(img, "rb"))}

    r = requests.post("https://starkapi.herokuapp.com/nsfw/", files=f).json()
    if r.get("success") is False:
        is_nsfw = False
    elif r.get("is_nsfw") is True:
        is_nsfw = True
    elif r.get("is_nsfw") is False:
        is_nsfw = False
    return is_nsfw


@tbot.on(events.NewMessage(pattern="/gshield (.*)"))
async def nsfw_watch(event):
    if not event.is_group:
        await event.reply("Yᴏᴜ ᴄᴀɴ ᴏɴʟʏ NSFW ᴡᴀᴛᴄʜ ɪɴ ɢʀᴏᴜᴘs.")
        return
    input_str = event.pattern_match.group(1)
    if not await is_admin(event, BOT_ID):
        await event.reply("`I sʜᴏɪʟᴅ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ᴛʜɪs!`")
        return
    if await is_admin(event, event.message.sender_id):
        if (
            input_str == "on"
            or input_str == "On"
            or input_str == "ON"
            or input_str == "enable"
        ):
            if is_nsfwatch_indb(str(event.chat_id)):
                await event.reply("`Tʜɪs ᴄʜᴀᴛ ʜᴀs ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ NSFW ᴡᴀᴛᴄʜ.`")
                return
            add_nsfwatch(str(event.chat_id))
            await event.reply(
                f"**Aᴅᴅᴇᴅ ᴄʜᴀᴛ {event.chat.title} ᴡɪᴛʜ ɪᴅ {event.chat_id} ᴛᴏ ᴅᴀᴛᴀʙᴀsᴇ. Tʜɪs ɢʀᴏᴜᴘs NSFW ᴄᴏɴᴛᴇɴᴛs ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ʙʏ ᴍᴇ ғʀᴏᴍ ɴᴏᴡ**"
            )
        elif (
            input_str == "off"
            or input_str == "Off"
            or input_str == "OFF"
            or input_str == "disable"
        ):
            if not is_nsfwatch_indb(str(event.chat_id)):
                await event.reply("Tʜɪs ᴄʜᴀᴛ ʜᴀs ɴᴏᴛ ᴇɴᴀʙʟᴇᴅ NSFW ᴡᴀᴛᴄʜ.")
                return
            rmnsfwatch(str(event.chat_id))
            await event.reply(
                f"**Rᴇᴍᴏᴠᴇᴅ ᴄʜᴀᴛ {event.chat.title} ᴡɪᴛʜ ɪᴅ {event.chat_id} ғʀᴏᴍ NSFW ᴡᴀᴛᴄʜ**"
            )
        else:
            await event.reply(
                "I ᴜɴᴅᴇʀsᴛᴀᴍᴅ `/nsfwguardian on` ᴀɴᴅ `/nsfwguardian off` ᴏɴʟʏ"
            )
    else:
        await event.reply("`Yᴏᴜ sʜᴏᴜʟᴅ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ᴛʜɪs!`")
        return


approved_users = db.approve
spammers = db.spammer
globalchat = db.globchat

CMD_STARTERS = ["/", "!", "."]
profanity.load_censor_words_from_file("./profanity_wordlist.txt")


@register(pattern="^/profanity(?: |$)(.*)")
async def profanity(event):
    if event.fwd_from:
        return
    if not event.is_group:
        await event.reply("Yᴏᴜ ᴄᴀɴ ᴏɴʟʏ ᴀᴄᴛɪᴠᴀᴛᴇ ᴘʀᴏғᴀɴɪᴛʏ ɪɴ ɢʀᴏᴜᴘs.")
        return
    event.pattern_match.group(1)
    if not await is_admin(event, BOT_ID):
        await event.reply("`I sʜᴏᴜʟᴅ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ᴛʜɪs!`")
        return
    if await is_admin(event, event.message.sender_id):
        input = event.pattern_match.group(1)
        chats = spammers.find({})
        if not input:
            for c in chats:
                if event.chat_id == c["id"]:
                    await event.reply(
                        "Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ sᴏᴍᴇ ɪɴᴘᴜᴛ yes ᴏʀ no.\n\nCᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴɢ ɪs : **on**"
                    )
                    return
            await event.reply(
                "Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ sᴏᴍᴇ ɪɴᴘᴜᴛ yes ᴏʀ no.\n\nCᴜʀʀᴇᴍᴛ sᴇᴛᴛɪɴɢ ɪs : **off**"
            )
            return
        if input == "on":
            if event.is_group:
                chats = spammers.find({})
                for c in chats:
                    if event.chat_id == c["id"]:
                        await event.reply(
                            "Pʀᴏғᴀɴɪᴛʏ ғɪʟᴛᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ."
                        )
                        return
                spammers.insert_one({"id": event.chat_id})
                await event.reply("Pʀᴏғᴀɴɪᴛʏ ғɪʟᴛᴇʀ ᴛᴜʀɴᴇᴅ ᴏɴ ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ.")
        if input == "off":
            if event.is_group:
                chats = spammers.find({})
                for c in chats:
                    if event.chat_id == c["id"]:
                        spammers.delete_one({"id": event.chat_id})
                        await event.reply("Pʀᴏғᴀɴɪᴛʏ ғɪʟᴛᴇʀ ᴛᴜʀɴᴇᴅ ᴏғғ ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ.")
                        return
            await event.reply("Pʀᴏғᴀɴɪᴛʏ ғɪʟᴛᴇʀ ɪsɴ'ᴛ ᴛᴜʀɴᴇᴅ ᴏɴ ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ.")
        if not input == "on" and not input == "off":
            await event.reply("I ᴏɴʟʏ ᴜɴᴅᴇʀsᴛᴀɴᴅ ʙʏ on ᴏʀ off")
            return
    else:
        await event.reply("`Yᴏᴜ sʜᴏᴜʟᴅ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ᴛʜɪs!`")
        return


@register(pattern="^/globalmode(?: |$)(.*)")
async def profanity(event):
    if event.fwd_from:
        return
    if not event.is_group:
        await event.reply("Yᴏᴜ ᴄᴀɴ ᴏɴʟʏ ᴇɴᴀʙʟᴇ ɢʟᴏʙᴀʟ ᴍᴏᴅᴇ ᴡᴀᴛᴄʜ ɪɴ ɢʀᴏᴜᴘs.")
        return
    event.pattern_match.group(1)
    if not await is_admin(event, BOT_ID):
        await event.reply("`I sʜᴏᴜʟᴅ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ᴛʜɪs!`")
        return
    if await is_admin(event, event.message.sender_id):

        input = event.pattern_match.group(1)
        chats = globalchat.find({})
        if not input:
            for c in chats:
                if event.chat_id == c["id"]:
                    await event.reply(
                        "Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ sᴏᴍᴇ ɪɴᴘᴜᴛ yes ᴏʀ no.\n\nCᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴɢ ɪs : **on**"
                    )
                    return
            await event.reply(
                "Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ sᴏᴍᴇ ɪɴᴘᴜᴛ yes ᴏʀ no.\n\nCᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴɢ ɪs : **off**"
            )
            return
        if input == "on":
            if event.is_group:
                chats = globalchat.find({})
                for c in chats:
                    if event.chat_id == c["id"]:
                        await event.reply(
                            "Gʟᴏʙᴀʟ ᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ."
                        )
                        return
                globalchat.insert_one({"id": event.chat_id})
                await event.reply("Gʟᴏʙᴀʟ ᴍᴏᴅᴇ ᴛᴜʀɴᴇᴅ ᴏɴ ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ.")
        if input == "off":
            if event.is_group:
                chats = globalchat.find({})
                for c in chats:
                    if event.chat_id == c["id"]:
                        globalchat.delete_one({"id": event.chat_id})
                        await event.reply("Gʟᴏʙᴀʟ ᴍᴏᴅᴇ ᴛᴜʀɴᴇᴅ ᴏғғ ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ.")
                        return
            await event.reply("Gʟᴏʙᴀʟ ᴍᴏᴅᴇ ɪsɴ'ᴛ ᴛᴜʀɴᴇᴅ ᴏɴ ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ.")
        if not input == "on" and not input == "off":
            await event.reply("I ᴏɴʟʏ ᴜɴᴅᴇʀsᴛᴀᴍᴅ ᴏɴ ᴏʀ ᴏғғ")
            return
    else:
        await event.reply("`Bʀᴏᴛʜᴇʀ, ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴜ ᴛʜɪs!`")
        return


@tbot.on(events.NewMessage(pattern=None))
async def del_profanity(event):
    if event.is_private:
        return
    msg = str(event.text)
    sender = await event.get_sender()
    # let = sender.username
    if await is_admin(event, event.message.sender_id):
        return
    chats = spammers.find({})
    for c in chats:
        if event.text:
            if event.chat_id == c["id"]:
                if better_profanity.profanity.contains_profanity(msg):
                    await event.delete()
                    if sender.username is None:
                        st = sender.first_name
                        hh = sender.id
                        final = f"[{st}](tg://user?id={hh}) **{msg}** ɪs ᴅᴇᴛᴇᴄᴛᴇᴅ ᴀs ᴀ sʟᴀɴɢ ᴡᴏʀᴅ ᴀɴᴅ ʏᴏᴜʀ ᴍsɢ ʜᴀs ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ. ʟᴏʟ"
                    else:
                        final = f"Sᴜʀʀʀ **{msg}** ɪs ᴅᴇᴛᴇᴄᴛᴇᴅ ᴀs ᴀ sʟᴀɴɢ ᴡᴏʀᴅ ᴀɴᴅ ʏᴏᴜʀ ᴍsɢ ʜᴀs ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ. ʟᴏʟ"
                    dev = await event.respond(final)
                    await asyncio.sleep(50)
                    await dev.delete()
        if event.photo:
            if event.chat_id == c["id"]:
                await event.client.download_media(event.photo, "nudes.jpg")
                if nude.is_nude("./nudes.jpg"):
                    await event.delete()
                    st = sender.first_name
                    hh = sender.id
                    final = f"**NSFW DETECTED**\n\n{st}](tg://user?id={hh}) Yᴏᴜʀ ᴍsɢ ᴄᴏɴᴛᴀɪɴ NSFW ᴄᴏᴍᴛᴇɴᴛ.. Sᴏ, Tᴇᴅᴅʏ ᴅᴇʟᴇᴛᴇs ᴛʜᴇ ᴍsɢ\n\n **Nsғᴡ Sᴇɴᴅᴇʀ - User / Bot :** {st}](tg://user?id={hh})  \n\n`⚔️Aᴜᴛᴏᴍᴀᴛɪᴄ ᴅᴇᴛᴇᴄᴛɪᴏɴs ᴘᴏᴡᴇʀᴇᴅ ʙʏ Tᴇᴅᴅʏ` \n**#GROUP_GUARDIAN** "
                    dev = await event.respond(final)
                    await asyncio.sleep(10)
                    await dev.delete()
                    os.remove("nudes.jpg")


def extract_emojis(s):
    return "".join(c for c in s if c in emoji.UNICODE_EMOJI)


@tbot.on(events.NewMessage(pattern=None))
async def del_profanity(event):
    if event.is_private:
        return
    msg = str(event.text)
    sender = await event.get_sender()
    # sender.username
    if await is_admin(event, event.message.sender_id):
        return
    chats = globalchat.find({})
    for c in chats:
        if event.text:
            if event.chat_id == c["id"]:
                u = msg.split()
                emj = extract_emojis(msg)
                msg = msg.replace(emj, "")
                if (
                    [(k) for k in u if k.startswith("@")]
                    and [(k) for k in u if k.startswith("#")]
                    and [(k) for k in u if k.startswith("/")]
                    and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
                ):
                    h = " ".join(filter(lambda x: x[0] != "@", u))
                    km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
                    tm = km.split()
                    jm = " ".join(filter(lambda x: x[0] != "#", tm))
                    hm = jm.split()
                    rm = " ".join(filter(lambda x: x[0] != "/", hm))
                elif [(k) for k in u if k.startswith("@")]:
                    rm = " ".join(filter(lambda x: x[0] != "@", u))
                elif [(k) for k in u if k.startswith("#")]:
                    rm = " ".join(filter(lambda x: x[0] != "#", u))
                elif [(k) for k in u if k.startswith("/")]:
                    rm = " ".join(filter(lambda x: x[0] != "/", u))
                elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
                    rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
                else:
                    rm = msg
                # print (rm)
                b = translator.detect(rm)
                if not "en" in b and not b == "":
                    await event.delete()
                    st = sender.first_name
                    hh = sender.id
                    final = f"[{st}](tg://user?id={hh}) Yᴏᴜ sʜᴏᴜʟᴅ ᴏɴʟʏ sᴘᴇᴀᴋ ɪɴ ᴇɴɢ ʜᴇʀᴇ !"
                    dev = await event.respond(final)
                    await asyncio.sleep(10)
                    await dev.delete()

__mod_name__ = "Shield"
