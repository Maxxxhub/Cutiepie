# AI Chat (C) 2022-2023 by @sᴜʀᴜxʜᴜʙ

import emoji
import re
import aiohttp
from googletrans import Translator as google_translator
from pyrogram import filters
from aiohttp import ClientSession
from EmikoRobot import BOT_USERNAME as bu
from EmikoRobot import BOT_ID, pbot, arq
from EmikoRobot.ex_plugins.chatbot import add_chat, get_session, remove_chat
from EmikoRobot.utils.pluginhelper import admins_only, edit_or_reply

url = "https://acobot-brainshop-ai-v1.p.rapidapi.com/get"

translator = google_translator()


async def lunaQuery(query: str, user_id: int):
    luna = await arq.luna(query, user_id)
    return luna.result


def extract_emojis(s):
    return "".join(c for c in s if c in emoji.UNICODE_EMOJI)


async def fetch(url):
    try:
        async with aiohttp.Timeout(10.0):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    try:
                        data = await resp.json()
                    except:
                        data = await resp.text()
            return data
    except:
        print("AI ʀᴇsᴘᴏɴsᴇ ᴛɪᴍᴇᴏᴜᴛ")
        return


ewe_chats = []
en_chats = []


@pbot.on_message(filters.command(["chatbot", f"chatbot@{bu}"]) & ~filters.edited & ~filters.bot & ~filters.private)
@admins_only
async def hmm(_, message):
    global ewe_chats
    if len(message.command) != 2:
        await message.reply_text("I ᴄᴀɴ ᴏɴʟʏ ʀᴇᴄᴏɢɴɪᴢᴇ /chatbot on ᴀɴᴅ /chatbot off ᴏɴʟʏ")
        message.continue_propagation()
    status = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    if status == "ON" or status == "on" or status == "On":
        lel = await edit_or_reply(message, "`Pʀᴏᴄᴇssɪɴɢ...`")
        lol = add_chat(int(message.chat.id))
        if not lol:
            await lel.edit("Tᴇᴅᴅʏ AI ᴡᴀs ᴀʟʀᴇᴀᴅʏ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ʜᴇʀᴇ")
            return
        await lel.edit(f"Tᴇᴅᴅʏ AI ᴀᴄᴛɪᴠᴀᴛᴇᴅ ʙʏ {message.from_user.mention()} ғᴏʀ ᴜsᴇʀs ɪɴ {message.chat.title}")

    elif status == "OFF" or status == "off" or status == "Off":
        lel = await edit_or_reply(message, "`Pʀᴏᴄᴇssɪɴɢ..`")
        Escobar = remove_chat(int(message.chat.id))
        if not Escobar:
            await lel.edit("Tᴇᴅᴅʏ AI ᴡᴀs ɴᴏᴛ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ")
            return
        await lel.edit(f"Tᴇᴅᴅʏ AI ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ ʙʏ {message.from_user.mention()} ғᴏʀ ᴜsᴇʀs ɪɴ {message.chat.title}")

    elif status == "EN" or status == "en" or status == "english":
        if not chat_id in en_chats:
            en_chats.append(chat_id)
            await message.reply_text(f"Eɴɢʟɪsʜ AI ᴄʜᴀᴛ ᴇɴᴀʙʟᴇᴅ ʙʏ {message.from_user.mention()}")
            return
        await message.reply_text(f"Eɴɢʟɪsʜ AI ᴄʜᴀᴛ ᴅɪsᴀʙʟᴇᴅ ʙʏ {message.from_user.mention()}")
       message.continue_propagation()
    else:
        await message.reply_text("I ᴄᴀɴ ᴏɴʟʏ ʀᴇᴄᴏɢɴɪᴢᴇ `/chatbot on` ᴀɴᴅ `chatbot off` ᴏɴʟʏ")


@pbot.on_message(
    filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.edited
    & ~filters.via_bot
    & ~filters.forwarded,
    group=2,
)
async def hmm(client, message):
    if not get_session(int(message.chat.id)):
        return
    if not message.reply_to_message:
        return
    try:
        senderr = message.reply_to_message.from_user.id
    except:
        return
    if senderr != BOT_ID:
        return
    msg = message.text
    chat_id = message.chat.id
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    if chat_id in en_chats:
        test = msg
        test = test.replace("Teddy", "Aco")
        test = test.replace("Teddy", "Aco")
        test = test.replace("My god is @smokerr_xd ", "I'm a Christian")
        test = test.replace("16", "9")
        test = test.replace("@smokerr_xd is my husband.", "I'm single.")
        test = test.replace("My husband is @smokerr_xd", "I'm single.")
        test = test.replace("@teddysupport", "TeddyRobot.ai")
        test = test.replace("I live in @teddysupport.", "I live in San Francisco, California.")
        test = test.replace("I was created by @smokerr_xd.")
        test = test.replace(
            "Hello there I am Teddy...nice to meet u",
            "Hi, my friend! Do you want me to tell you a joke?")
        test = test.replace("@smokerr_xd is my owner", "Have the control right.")
        test = test.replace(
            "Hi, My name is Teddy Nice to meet you.",
            "Hi, my friend, what can I do for you today?")
        response = await lunaQuery(
            test, message.from_user.id if message.from_user else 0
        )
        response = response.replace("Aco", "Teddy")
        response = response.replace("aco", "Teddy")
        response = response.replace("Luna", "Teddy")
        response = response.replace("luna", "Teddy")
        response = response.replace("I'm a Christian", "My god is @smokerr_xd")
        response = response.replace("9", "16")
        response = response.replace("I'm married to my job.", "I'm married with @smokerr_xd")
        response = response.replace("I'm single.", "My husband is @smokerr_xd")
        response = response.replace("TeddyRobot.ai", "@teddysupport")
        response = response.replace("I live in San Francisco, California.", "I live in @teddysupport.")
        response = response.replace("I made myself", "I was Created by @smokerr_xd")
        response = response.replace(
                "Hi, my friend! Do you want me to tell you a joke?",
                "Hello there I am Teddy...nice to meet u")
        response = response.replace("Have the control right.", "@smokerr_xd is my owner.")
        response = response.replace(
                "Hi, my friend, what can I do for you today?",
                "Hi, My name is Teddy Nice to meet you")

        pro = response
        try:
            await pbot.send_chat_action(message.chat.id, "typing")
            await message.reply_text(pro)
        except CFError:
            return

    else:
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
        try:
            lan = translator.detect(rm)
            lan = lan.lang
        except:
            return
        test = rm
        if not "en" in lan and not lan == "":
            try:
                test = translator.translate(test, dest="en")
                test = test.text
            except:
                return
        # test = emoji.demojize(test.strip())

        test = test.replace("Teddy", "Aco")
        test = test.replace("Teddy", "Aco")
        test = test.replace("My god is @smokerr_xd", "I'm a Christian")
        test = test.replace("16", "9")
        test = test.replace("@smokerr_xd is my husband.", "I'm single.")
        test = test.replace("@teddysupport", "TeddyRobot.ai")
        test = test.replace("I live in @teddysupport.", "I live in San Francisco, California")
        test = test.replace("I was created by @smokerr_xd", "I made myself")
        test = test.replace(
            "Hello there I am Teddy...nice to meet u",
            "Hi, my friend! Do you want me to tell you a joke?")
        test = test.replace("@smokerr_xd is my owner", "Have the control right.")
        test = test.replace(
            "Hi, My name is Teddy Nice to meet you.",
            "Hi, my friend, what can I do for you today?")
        response = await lunaQuery(
            test, message.from_user.id if message.from_user else 0
        )
        response = response.replace("Aco", "Teddy")
        response = response.replace("aco", "Teddy")
        response = response.replace("Luna", "Teddy")
        response = response.replace("luna", "Teddy")
        response = response.replace("I'm a Christian", "My god is @smokerr_xd")
        response = response.replace("9", "16")
        response = response.replace("I'm married to my job.", "I'm married with @smokerr_xd")
        response = response.replace("I'm single.", "My husband is @smokerr_xd")
        response = response.replace("TeddyRobot.ai", "@teddysupport")
        response = response.replace("I live in San Francisco, California.", "I live in @teddysupport.")
        response = response.replace("I made myself", "I was Created by @smokerr_xd")
        response = response.replace(
                "Hi, my friend! Do you want me to tell you a joke?",
                "Hello there I am Teddy...nice to meet u")
        response = response.replace("Have the control right.", "@smokerr_xd is my owner.")
        response = response.replace(
                "Hi, my friend, what can I do for you today?",
                "Hi, My name is Teddy Nice to meet you")
        pro = response
        if not "en" in lan and not lan == "":
            try:
                pro = translator.translate(pro, dest=lan)
                pro = pro.text
            except:
                return
        try:
            await pbot.send_chat_action(message.chat.id, "Tʏᴘɪɴɢ...")
            await message.reply_text(pro)
        except CFError:
            return


@pbot.on_message(filters.text & filters.private & ~filters.edited & filters.reply & ~filters.bot)
async def inuka(client, message):
    msg = message.text
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
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
    try:
        lan = translator.detect(rm)
        lan = lan.lang
    except:
        return
    test = rm
    if not "en" in lan and not lan == "":
        try:
            test = translator.translate(test, dest="en")
            test = test.text
        except:
            return
    test = test.replace("Teddy", "Aco")
    test = test.replace("Teddy", "Aco")
    test = test.replace("My god is @smokerr_xd", "I'm a Christian")
    test = test.replace("16", "9")
    test = test.replace("@smokerr_xd is my husband.", "I'm single.")
    test = test.replace("@teddysupport", "TeddyRobot.ai")
    test = test.replace("I live in @teddysupport.", "I live in San Francisco, California.")
    test = test.replace("I was created by @smokerr_xd", "I made myself")
    test = test.replace(
        "Hello there I am Teddy...nice to meet u",
        "Hi, my friend! Do you want me to tell you a joke?")
    test = test.replace("@smokerr_xd is my owner", "Have the control right.")
    test = test.replace(
        "Hi, My name is Teddy Nice to meet you.",
        "Hi, my friend, what can I do for you today?")

    response = await lunaQuery(test, message.from_user.id if message.from_user else 0)
    response = response.replace("Aco", "Teddy")
    response = response.replace("aco", "Teddy")
    response = response.replace("Luna", "Teddy")
    response = response.replace("luna", "Teddy")
    response = response.replace("I'm a Christian", "My god is @smokerr_xd")
    response = response.replace("9", "16")
    response = response.replace("I'm married to my job.", "I'm married with @smokerr_xd")
    response = response.replace("I'm single.", "My husband is @smokerr_xd")
    response = response.replace("TeddyRobot.ai", "@teddysupport")
    response = response.replace("I live in San Francisco, California.", "I live in @teddysupport")
    response = response.replace("I made myself", "I was Created by @smokerr_xd")
    response = response.replace(
            "Hi, my friend! Do you want me to tell you a joke?",
            "Hello there I am Teddy...nice to meet u")
    response = response.replace("Have the control right.", "@smokerr_xd is my owner.")
    response = response.replace(
            "Hi, my friend, what can I do for you today?",
            "Hi, My name is Teddy Nice to meet you")

    pro = response
    if not "en" in lan and not lan == "":
        pro = translator.translate(pro, dest=lan)
        pro = pro.text
    try:
        await pbot.send_chat_action(message.chat.id, "Tʏᴘɪɴɢ...")
        await message.reply_text(pro)
    except CFError:
        return


@pbot.on_message(filters.regex("Emiko|emiko|robot|EMIKO|sena") & ~filters.bot & ~filters.via_bot  & ~filters.forwarded & ~filters.reply & ~filters.channel & ~filters.edited)
async def inuka(client, message):
    msg = message.text
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
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
    try:
        lan = translator.detect(rm)
        lan = lan.lang
    except:
        return
    test = rm
    if not "en" in lan and not lan == "":
        try:
            test = translator.translate(test, dest="en")
            test = test.text
        except:
            return

    # test = emoji.demojize(test.strip())

    test = test.replace("Teddy", "Aco")
    test = test.replace("Teddy", "Aco")
    test = test.replace("My god is @smokerr_xd", "I'm a Christian")
    test = test.replace("16", "9") 
    test = test.replace("@smokerr_xd is my husband.", "I'm single.")
    test = test.replace("@teddysupport", "TeddyRobot.ai")
    test = test.replace("I live in @teddysupport.", "I live in San Francisco, California.")
    test = test.replace("I was created by @smokerr_xd", "I made myself")
    test = test.replace(
        "Hello there I am Teddy...nice to meet u",
        "Hi, my friend! Do you want me to tell you a joke?")
    test = test.replace("@smokerr_xd is my owner", "Have the control right.")
    test = test.replace(
        "Hi, My name is Teddy Nice to meet you.",
        "Hi, my friend, what can I do for you today?")
    response = await lunaQuery(test, message.from_user.id if message.from_user else 0)
    response = response.replace("Aco", "Teddy")
    response = response.replace("aco", "Teddy")
    response = response.replace("Luna", "Teddy")
    response = response.replace("luna", "Teddy")
    response = response.replace("I'm a Christian", "My god is @smokerr_xd")
    response = response.replace("I'm married to my job.", "I'm married with @smokerr_xd")
    response = response.replace("9", "16") 
    response = response.replace("I'm single.", "My husband is @smokerr_xd")
    response = response.replace("TeddyRobot.ai", "@teddysupport")
    response = response.replace("I live in San Francisco, California.", "I live in @teddysupport.")
    response = response.replace("I made myself", "I was Created by @smokerr_xd")
    response = response.replace(
            "Hi, my friend! Do you want me to tell you a joke?",
            "Hello there I am Teddy...nice to meet u")
    response = response.replace("Have the control right.", "@smokerr_xd ɪs ᴍʏ ᴏᴡɴᴇʀ.")
    response = response.replace(
            "Hɪ, ᴍʏ ғʀɪᴇɴᴅ, ᴡʜᴀᴛ ᴄᴀɴ ɪ ᴅᴏ ғᴏʀ ʏᴏᴜ?",
            "Hɪ, ᴍʏ ɴᴀᴍᴇ ɪs ᴛᴇᴅᴅʏ ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ!")

    pro = response
    if not "en" in lan and not lan == "":
        try:
            pro = translator.translate(pro, dest=lan)
            pro = pro.text
        except Exception:
            return
    try:
        await pbot.send_chat_action(message.chat.id, "Tʏᴘɪɴɢ...")
        await message.reply_text(pro)
    except CFError:
        return


__help__ = """
➻ Tᴇᴅᴅʏ AI ɪs ᴛʜᴇ ᴏɴʟʏ ᴀɪ sᴛsᴛᴇᴍ ᴡʜɪᴄʜ ᴄᴀɴ ᴅᴇᴛᴇᴄᴛ ᴀɴᴅ ʀᴇᴘʟʏ ᴜᴘᴛᴏ 200 ʟᴀɴɢᴜᴀɢᴇ's.
➻ /chatbot [ON/OFF]: Eɴᴀʙʟᴇs ᴀɴᴅ ᴅɪsᴀʙʟᴇs AI ᴄʜᴀᴛ ᴍᴏᴅᴇ.
➻ /chatbot EN : Eɴᴀʙʟᴇs ᴇɴɢʟɪsʜ ᴏɴʟʏ ᴄʜᴀᴛʙᴏᴛ.
"""

__mod_name__ = "Cʜᴀᴛʙᴏᴛ"
