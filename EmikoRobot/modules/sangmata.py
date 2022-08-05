from telethon.errors.rpcerrorlist import YouBlockedUserError
from EmikoRobot import telethn as tbot
from EmikoRobot.events import register
from EmikoRobot import ubot2 as ubot
from asyncio.exceptions import TimeoutError


@register(pattern="^/sg ?(.*)")
@register(pattern="^/check_name ?(.*)")
async def lastname(steal):
    steal.pattern_match.group(1)
    puki = await steal.reply("```Rᴇᴛʀɪᴠɪɴɢ sᴜᴄʜ ᴜsᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ..Pʟᴇᴀsᴇ ᴡᴀɪᴛ ❄️```")
    if steal.fwd_from:
        return
    if not steal.reply_to_msg_id:
        await puki.edit("```Pʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴜsᴇʀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴄʜᴇᴄᴋ ᴛʜᴇɪʀ ɴᴀᴍᴇ ʜɪsᴛᴏʀʏ ❗```")
        return
    message = await steal.get_reply_message()
    chat = "@SangMataInfo_bot"
    user_id = message.sender.id
    id = f"/search_id {user_id}"
    if message.sender.bot:
        await puki.edit("```Rᴇᴘʟʏ ᴛᴏ ʀᴇᴀʟ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ.!```")
        return
    await puki.edit("```Pʟᴇᴀsᴇ ᴡᴀɪᴛ ❄️...```")
    try:
        async with ubot.conversation(chat) as conv:
            try:
                msg = await conv.send_message(id)
                r = await conv.get_response()
                response = await conv.get_response()
            except YouBlockedUserError:
                await steal.reply(
                    "```Eʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ᴛʜɪs ᴛᴏ @Teddysupport```"
                )
                return
            if r.text.startswith("Name"):
                respond = await conv.get_response()
                await puki.edit(f"`{r.message}`")
                await ubot.delete_messages(
                    conv.chat_id, [msg.id, r.id, response.id, respond.id]
                ) 
                return
            if response.text.startswith("No records") or r.text.startswith(
                "No records"
            ):
                await puki.edit("```I ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ's ɪɴғᴏʀᴍᴀᴛɪᴏɴ, Tʜɪs ᴜsᴇʀ ʜᴀs ɴᴇᴠᴇʀ ᴄʜᴀɴɢᴇᴅ ᴛʜᴇɪʀ ɴᴀᴍᴇ ʙᴇғᴏʀᴇ ❗.```")
                await ubot.delete_messages(
                    conv.chat_id, [msg.id, r.id, response.id]
                )
                return
            else:
                respond = await conv.get_response()
                await puki.edit(f"```{response.message}```")
            await ubot.delete_messages(
                conv.chat_id, [msg.id, r.id, response.id, respond.id]
            )
    except TimeoutError:
        return await puki.edit("`I'ᴍ sɪᴄᴋ, sᴏʟʟʏ...🤐`")
