from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
import flag
import html, os
from countryinfo import CountryInfo
from EmikoRobot import telethn as borg
from EmikoRobot.events import register


@register(pattern="^/country (.*)")
async def msg(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    lol = input_str
    country = CountryInfo(lol)
    try:
        a = country.info()
    except:
        await event.reply("Cᴏᴜɴᴛʀʏ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴜʀᴇᴇɴᴛʟʏ")
    name = a.get("name")
    bb = a.get("altSpellings")
    hu = ""
    for p in bb:
        hu += p + ",  "

    area = a.get("area")
    borders = ""
    hell = a.get("borders")
    for fk in hell:
        borders += fk + ",  "

    call = ""
    WhAt = a.get("callingCodes")
    for what in WhAt:
        call += what + "  "

    capital = a.get("capital")
    currencies = ""
    fker = a.get("currencies")
    for FKer in fker:
        currencies += FKer + ",  "

    HmM = a.get("demonym")
    geo = a.get("geoJSON")
    pablo = geo.get("features")
    Pablo = pablo[0]
    PAblo = Pablo.get("geometry")
    EsCoBaR = PAblo.get("type")
    iso = ""
    iSo = a.get("ISO")
    for hitler in iSo:
        po = iSo.get(hitler)
        iso += po + ",  "
    fla = iSo.get("alpha2")
    nox = fla.upper()
    okie = flag.flag(nox)

    languages = a.get("languages")
    lMAO = ""
    for lmao in languages:
        lMAO += lmao + ",  "

    nonive = a.get("nativeName")
    waste = a.get("population")
    reg = a.get("region")
    sub = a.get("subregion")
    tik = a.get("timezones")
    tom = ""
    for jerry in tik:
        tom += jerry + ",   "

    GOT = a.get("tld")
    lanester = ""
    for targaryen in GOT:
        lanester += targaryen + ",   "

    wiki = a.get("wiki")

    caption = f"""<b><u>Iɴғᴏʀᴍᴀᴛɪᴏɴ ɢᴀᴛʜᴇʀᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ 🚩</b></u>
<b>
Cᴏᴜɴᴛʀʏ ɴᴀᴍᴇ:- {name}
Aʟᴛᴇʀɴᴀᴛɪᴠᴇ sᴘᴇʟʟɪɴɢs:- {hu}
Cᴏᴜɴᴛʀʏ ᴀʀᴇᴀ:- {area} sǫᴜᴀʀᴇ ᴋɪʟᴏᴍᴇᴛᴇʀs
Bᴏʀᴅᴇʀs:- {borders}
Cᴀʟʟɪɴɢ ᴄᴏᴅᴇs:- {call}
Cᴏᴜɴᴛʀʏ's ᴄᴀᴘɪᴛᴀʟ:- {capital}
Cᴏᴜɴᴛʀʏ's ᴄᴜʀʀᴇɴᴄʏ:- {currencies}
Cᴏᴜɴᴛʀʏ's ғʟᴀɢ:- {okie}
Dᴇᴍᴏɴʏᴍ:- {HmM}
Cᴏᴜɴᴛʀʏ ᴛʏᴘᴇ:- {EsCoBaR}
ISO Nᴀᴍᴇs:- {iso}
Lᴀɴɢᴜᴀɢᴇs:- {lMAO}
Nᴀᴛɪᴠᴇ ɴᴀᴍᴇ:- {nonive}
Pᴏᴜʟᴀᴛɪᴏɴ:- {waste}
Rᴇɢɪᴏɴ:- {reg}
Sᴜʙ ʀᴇɢɪᴏɴ:- {sub}
Tɪᴍᴇ ᴢᴏɴᴇs:- {tom}
Tᴏᴘ ʟᴇᴠᴇʟ ᴅᴏᴍᴀɪɴ:- {lanester}
Wɪᴋɪᴘᴇᴅɪᴀ:- {wiki}</b>
Gᴀᴛʜᴇʀᴇᴅ ʙʏ @Teddysupport 🖤.</b>
"""

    await borg.send_message(
        event.chat_id,
        caption,
        parse_mode="HTML",
    )

    await event.delete()
    
__help__ = """
I ᴄᴀɴ ɢɪᴠᴇ ʏᴏᴜ ᴀɴ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴏғ ᴀ ʏ ᴄᴏᴜɴᴛʀʏ.\nSᴇᴇ ʙᴇʟᴏᴡ ғᴏʀ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴍᴍᴀɴᴅs.!

× /country <country name>: Tᴏ ɢᴀᴛʜᴇʀ ᴀɴ ɪɴғᴏ ᴀʙᴏᴜᴛ ɢᴏᴠᴇᴍ ᴄᴏᴜɴᴛʀʏ """
    
__mod_name__ = "Cᴏᴜɴᴛʀʏ"
    
