import asyncio
from pyrogram import filters
from aiohttp import ClientSession
from Python_ARQ import ARQ

from EmikoRobot import pbot as app, BOT_ID
from EmikoRobot.utils.errors import capture_err
from EmikoRobot.utils.permissions import adminsOnly
from EmikoRobot.ex_plugins.dbfunctions import (
    alpha_to_int,
    get_karma,
    get_karmas,
    int_to_alpha,
    is_karma_on,
    karma_off,
    karma_on,
    update_karma,
)      
from EmikoRobot.utils.filter_groups import karma_negative_group, karma_positive_group
from EmikoRobot import arq

regex_upvote = r"^((?i)\+|\+\+|\+1|thx|nice|thanx|thanks|pro|cool|good|👍|piro|impressive|op)$"
regex_downvote = r"^(\-|\-\-|\-1|👎|noob|weak|chutiya|noobs|chutiye|bad)$"



@app.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_upvote)
    & ~filters.via_bot
    & ~filters.bot
    & ~filters.edited,
    group=karma_positive_group,
)
@capture_err
async def upvote(_, message):
    if not await is_karma_on(message.chat.id):
        return
    if not message.reply_to_message.from_user:
        return
    if not message.from_user:
        return
    if message.reply_to_message.from_user.id == message.from_user.id:
        return
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    current_karma = await get_karma(
        chat_id, await int_to_alpha(user_id)
    )
    if current_karma:
        current_karma = current_karma['karma']
        karma = current_karma + 1
    else:
        karma = 1
    new_karma = {"karma": karma}
    await update_karma(
        chat_id, await int_to_alpha(user_id), new_karma
    )
    await message.reply_text(
        f"Iɴᴄʀᴇᴍᴇɴᴛᴇᴅ ᴋᴀʀᴍᴀ ᴏғ {user_mention} ʙʏ 1 \nTᴏᴛᴀʟ ᴘᴏɪɴᴛs: {karma}"
    )


@app.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_upvote)
    & ~filters.via_bot
    & ~filters.bot
    & ~filters.edited,
    group=karma_positive_group,
)
@capture_err
async def upvote(_, message):
    if not is_karma_on(message.chat.id):
        return
    if not message.reply_to_message.from_user:
        return
    if not message.from_user:
        return
    if message.reply_to_message.from_user.id == message.from_user.id:
        return
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
    if current_karma:
        current_karma = current_karma["karma"]
        karma = current_karma + 1
    else:
        karma = 1
    new_karma = {"karma": karma}
    await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    await message.reply_text(
        f"Iɴᴄʀᴇᴍᴇɴᴛᴇᴅ ᴋᴀʀᴍᴀ ᴏғ {user_mention} ʙʏ 1 \nTᴏᴛᴀʟ ᴘᴏɪɴᴛs: {karma}"
    )


@app.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_downvote)
    & ~filters.via_bot
    & ~filters.bot
    & ~filters.edited,
    group=karma_negative_group,
)
@capture_err
async def downvote(_, message):
    if not is_karma_on(message.chat.id):
        return
    if not message.reply_to_message.from_user:
        return
    if not message.from_user:
        return
    if message.reply_to_message.from_user.id == message.from_user.id:
        return

    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
    if current_karma:
        current_karma = current_karma["karma"]
        karma = current_karma - 1
    else:
        karma = 1
    new_karma = {"karma": karma}
    await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    await message.reply_text(
        f"Dᴇᴄʀᴇᴍᴇɴᴛᴇᴅ ᴋᴀʀᴍᴀ ᴏғ {user_mention} ʙʏ 1 \nTᴏᴛᴀʟ ᴘᴏɪɴᴛs: {karma}"
    )


@app.on_message(filters.command("karmastat") & filters.group)
@capture_err
async def karma(_, message):
    chat_id = message.chat.id
    if not message.reply_to_message:
        m = await message.reply_text("Aɴᴀʟʏᴢɪɴɢ ᴋᴀʀᴍᴀ...Wɪʟʟ ᴛᴀᴋᴇ 10 sᴇᴄ...")
        karma = await get_karmas(chat_id)
        if not karma:
            await m.edit("Nᴏ ᴋᴀʀᴍᴀ ɪɴ ᴍʏ DB ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ.")
            return
        msg = f"**Kᴀʀᴍᴀ ʟɪsᴛ ᴏғ {message.chat.title}:- **\n"
        limit = 0
        karma_dicc = {}
        for i in karma:
            user_id = await alpha_to_int(i)
            user_karma = karma[i]["karma"]
            karma_dicc[str(user_id)] = user_karma
            karma_arranged = dict(
                sorted(karma_dicc.items(), key=lambda item: item[1], reverse=True)
            )
        if not karma_dicc:
            await m.edit("Nᴏ ᴋᴀʀᴍᴀ ɪɴ ᴍʏ DB ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ.")
            return
        for user_idd, karma_count in karma_arranged.items():
            if limit > 9:
                break
            try:
                user = await app.get_users(int(user_idd))
                await asyncio.sleep(0.8)
            except Exception:
                continue
            first_name = user.first_name
            if not first_name:
                continue
            username = user.username
            msg += f"**{karma_count}**  {(first_name[0:12] + '...') if len(first_name) > 12 else first_name}  `{('@' + username) if username else user_idd}`\n"
            limit += 1
        await m.edit(msg)
    else:
        user_id = message.reply_to_message.from_user.id
        karma = await get_karma(chat_id, await int_to_alpha(user_id))
        karma = karma["karma"] if karma else 0
        await message.reply_text(f"**Tᴏᴛᴀʟ ᴘᴏɪɴᴛs**: __{karma}__")


@app.on_message(filters.command("karma") & ~filters.private)
@adminsOnly("can_change_info")
async def captcha_state(_, message):
    usage = "**Usᴀɢᴇ:**\n/kᴀʀᴍᴀ [ON|OFF]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "on":
        await karma_on(chat_id)
        await message.reply_text("Eɴᴀʙʟᴇᴅ ᴋᴀʀᴍᴀ sʏsᴛᴇᴍ.")
    elif state == "off":
        karma_off(chat_id)
        await message.reply_text("Dɪsᴀʙʟᴇᴅ ᴋᴀʀᴍᴀ sʏsᴛᴇᴍ.")
    else:
        await message.reply_text(usage)
