import aiohttp
from pyrogram import filters
from EmikoRobot import pbot, BOT_USERNAME
from EmikoRobot.utils.errors import capture_err


__help__ = """
I ᴄᴀɴ ɢɪᴠᴇ ʏᴏᴜ ᴀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ sᴏᴍᴇᴏɴᴇ's ɢɪᴛʜᴜʙ ᴘʀᴏғɪʟᴇ..Hᴇʀᴇ ᴀʀᴇ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs ғᴏʀ ɪᴛ.. 

 × /github <username>: Tᴏ ɢᴇᴛ ᴀ ᴡʜᴏʟᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀ ɢɪᴛʜᴜʙ ᴜsᴇʀ. """

__mod_name__ = "Gɪᴛʜᴜʙ"


@pbot.on_message(filters.command(["github", "git", f"git@{BOT_USERNAME}"]))
@capture_err
async def github(_, message):
    if len(message.command) != 2:
        await message.reply_text("/git Usᴇʀɴᴀᴍᴇ")
        return
    username = message.text.split(None, 1)[1]
    URL = f"https://api.github.com/users/{username}"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await message.reply_text("404")

            result = await request.json()
            try:
                url = result["html_url"]
                name = result["name"]
                company = result["company"]
                bio = result["bio"]
                created_at = result["created_at"]
                avatar_url = result["avatar_url"]
                blog = result["blog"]
                location = result["location"]
                repositories = result["public_repos"]
                followers = result["followers"]
                following = result["following"]
                caption = f"""**📍Iɴғᴏ ᴏғ {name}**
**🔰Usᴇʀɴᴀᴍᴇ:** `{username}`
**🌍Bɪᴏ:** `{bio}`
**🏠Pʀᴏғɪʟᴇ ʟɪɴᴋ:** [Yᴜᴘ, Cʟɪᴄᴋ ᴍᴇ]({url})
**💈Cᴏᴍᴘᴀɴʏ:** `{company}`
**🧐Cʀᴇᴀᴛᴇᴅ ᴏɴ:** `{created_at}`
**👨‍💻Rᴇᴘᴏsɪᴛᴏʀɪᴇs:** `{repositories}`
**♻️Bʟᴏɢ:** `{blog}`
**🌐Lᴏᴄᴀᴛɪᴏɴ:** `{location}`
**🚩Fᴏʟʟᴏᴡᴇʀs:** `{followers}`
**🔖Fᴏʟʟᴏᴡɪɴɢ:** `{following}`"""
            except Exception as e:
                print(str(e))
                pass
    await message.reply_photo(photo=avatar_url, caption=caption)
