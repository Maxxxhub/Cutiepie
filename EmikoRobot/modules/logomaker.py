import os
import io
import requests
import shutil 
import random
import re
import glob
import time

from io import BytesIO
from requests import get
from telethon.tl.types import InputMessagesFilterPhotos

from EmikoRobot import OWNER_ID, BOT_USERNAME, SUPPORT_CHAT
from EmikoRobot.events import register
from EmikoRobot import telethn
from PIL import Image, ImageDraw, ImageFont


LOGO_LINKS            = [
"https://telegra.ph/file/a6e24e61def1405d820db.jpg",
"https://telegra.ph/file/aae59ac05046b83439576.jpg",
"https://telegra.ph/file/7788ebff0346025010fc0.jpg",
"https://telegra.ph/file/1e5b7221953dd47d805e3.jpg",
"https://telegra.ph/file/f0c9993a1f5ec61a17195.jpg",
"https://telegra.ph/file/d89d7d045639f57c41c78.jpg",
"https://telegra.ph/file/47e70d33f86f2a8b83553.jpg",
"https://telegra.ph/file/615de6d5c1f3325b6cc31.jpg",
"https://telegra.ph/file/68e468c340e46d28d9359.jpg",
"https://telegra.ph/file/496fdb4bc28eb90ebe201.jpg",
"https://telegra.ph/file/e441362839a24d3e419e3.jpg",
"https://telegra.ph/file/0745f3315755a5399a95e.jpg",
"https://telegra.ph/file/a73bf0ad1b4b2adfecff1.jpg",
"https://telegra.ph/file/d52fa8c8fbcc885215a71.jpg",
"https://telegra.ph/file/17e670021f9099b9f4207.jpg",
"https://telegra.ph/file/1a6316d4d01d99cc6e223.jpg",
"https://telegra.ph/file/c8bbb75ff1e9832821024.jpg",
"https://telegra.ph/file/187b36280a49d651bf3e5.jpg",
"https://telegra.ph/file/a78e627734c4967b46a9f.jpg",
"https://telegra.ph/file/73282faf7f099469388ec.jpg",
"https://telegra.ph/file/60a8817e57de603dfae72.jpg"
"https://telegra.ph/file/282c6ab22e80ce45b4785.jpg",
"https://telegra.ph/file/d25bf93c8cf18ac41037f.jpg",
"https://telegra.ph/file/a14a0023842083a59b6ad.jpg",
"https://telegra.ph/file/65300b270360aae3acede.jpg",
"https://telegra.ph/file/5e50032a36dc1177f3a8d.jpg",
"https://telegra.ph/file/d7a13e6041d74559d11b0.jpg",
"https://telegra.ph/file/44e4ec30601f829def0da.jpg",
"https://telegra.ph/file/085f42b313030ff2fa2f0.jpg",
"https://telegra.ph/file/727b67f80c7bb4ae22738.jpg",
"https://telegra.ph/file/263c233fb1019fcfd9cca.jpg",
"https://telegra.ph/file/f3b2dca8ad0dee08e1bbe.jpg",
"https://telegra.ph/file/266868a200eb4638cbb7d.jpg",
"https://telegra.ph/file/abf24182aed7a1de31998.jpg",
"https://telegra.ph/file/7cd9e7467a6fcafeb195c.jpg",
"https://telegra.ph/file/a63c48047c512586ab476.jpg",
"https://telegra.ph/file/0a2dab693726f8af27b5f.jpg",
"https://telegra.ph/file/0b47f503353a1b78792f2.jpg",
"https://telegra.ph/file/b839316c2d27ce204595b.jpg",
"https://telegra.ph/file/fafd0f85c416dd83a8c58.jpg",
"https://telegra.ph/file/dd84b334e5384c9e0f1b9.jpg",
"https://telegra.ph/file/e9d191276c5f716f3e9e9.jpg",
"https://telegra.ph/file/d6434c9b4560e58ac9cd5.jpg",
"https://telegra.ph/file/b5eb75a1b21a74596391f.jpg",
"https://telegra.ph/file/7aa0ca1c3e7299915c05a.jpg",
"https://telegra.ph/file/72ec54e1497b191fad0fa.jpg",
"https://telegra.ph/file/f7f7155eb4edcaff76f74.jpg",
"https://telegra.ph/file/4c99e7cca16c3fb36242c.jpg",
"https://telegra.ph/file/fd20905cdb687e15ebde0.jpg",
"https://telegra.ph/file/59c13cecfca218539d20c.jpg",
"https://telegra.ph/file/cdc4a73861c990d8d0786.jpg",
"https://telegra.ph/file/75d0e94b22718c158d178.jpg",
"https://telegra.ph/file/d36dc8bf75cdf68689e39.jpg",
"https://telegra.ph/file/29a1327d3f6176f292754.jpg",
"https://telegra.ph/file/3bbb37579fccf06ffc625.jpg",
"https://telegra.ph/file/cd4b1450c682e8f0d75dd.jpg",
"https://telegra.ph/file/ecf1adaa0e63663b253cd.jpg",
"https://telegra.ph/file/36f69d4e445f3c0b15446.jpg",
"https://telegra.ph/file/764304ae41aba91a44a9b.jpg",
"https://telegra.ph/file/ced7e67449f59b0a069b1.jpg",
"https://telegra.ph/file/b5d44f449be9628451c04.jpg",
"https://telegra.ph/file/b6f8c2685fc338c02cfd3.jpg",
"https://telegra.ph/file/40abf21a416ab991aa4f9.jpg",
"https://telegra.ph/file/4e3602a3f5f0dd7f70a06.jpg",
"https://telegra.ph/file/803d27cd0b3232b90c296.jpg",
"https://telegra.ph/file/9d7fefb5005d18ad938b5.jpg",
"https://telegra.ph/file/2cefae27aad0151bb436a.jpg",
"https://telegra.ph/file/7af6683c32989f6ca2962.jpg",
"https://telegra.ph/file/a354c1dd55eed6f306bf9.jpg",
"https://telegra.ph/file/6aed5f88bdb2ac4604b56.jpg",
"https://telegra.ph/file/13fc4fa3d66608a946908.jpg",
"https://telegra.ph/file/a24bd77887c1dc5f79195.jpg",
"https://telegra.ph/file/ae2642afb2bb5d652e818.jpg",
"https://telegra.ph/file/08a34b304ecddc41effae.jpg",
"https://telegra.ph/file/47c8ca7d0e851f0095d1d.jpg",
"https://telegra.ph/file/8215dbb92de3f38ba6b6c.jpg",
"https://telegra.ph/file/456c383aafbede1be9dd7.jpg",
"https://telegra.ph/file/655ae719710ab66673cff.jpg",
"https://telegra.ph/file/149de7e129f77064429aa.jpg",
"https://telegra.ph/file/557925cd5c2886641a94d.jpg",
"https://telegra.ph/file/c18d8652bc39a594abfd9.jpg",
"https://telegra.ph/file/5f9826b4e81ba7918f349.jpg",
"https://telegra.ph/file/b5c6736de930c34561865.jpg",
"https://telegra.ph/file/14098ebcce48cc96bde1f.jpg",
"https://telegra.ph/file/42a1a83809de18d5b4f13.jpg",
"https://telegra.ph/file/4270c8522e6376e248d84.jpg",
"https://telegra.ph/file/c65b6820e9d59e56deb4e.jpg",
"https://telegra.ph/file/4a784f48d51715aae8676.jpg",
"https://telegra.ph/file/4e4a458ed45313054e3ba.jpg",
"https://telegra.ph/file/0d744c8699c395d313db4.jpg",
"https://telegra.ph/file/86fa7e9a534bd20caa889.jpg",
"https://telegra.ph/file/6b089118338c6df617623.jpg",
"https://telegra.ph/file/b081a57abfc5f121e4ddd.jpg",
"https://telegra.ph/file/83a1bd560c6255a932e60.jpg",
"https://telegra.ph/file/0b69352766e11244ad87b.jpg",
"https://telegra.ph/file/49c936107d6d600fc7a70.jpg",
"https://telegra.ph/file/7a5d56f4acf924d3b314f.jpg",
"https://telegra.ph/file/980bfdbeb8d323dc18cf0.jpg",
"https://telegra.ph/file/ad81c892562eaa0ad0da4.jpg",
"https://telegra.ph/file/cdb2367a5bf79073a70e6.jpg",
"https://telegra.ph/file/82920ff5292105125c0b0.jpg",
"https://telegra.ph/file/0c889f45fd82ff076dec1.jpg",
"https://telegra.ph/file/4da20d48bf42fabb4585c.jpg",
"https://telegra.ph/file/9129fac921eadedd034ad.jpg",
"https://telegra.ph/file/a16c9c337996d70634dfb.jpg",
"https://telegra.ph/file/017822ae5f4da9abcc012.jpg",
"https://telegra.ph/file/29ed7c273d33b8c0c943d.jpg",
"https://telegra.ph/file/6941556023df66ff076ad.jpg",
"https://telegra.ph/file/14804054c0de6a10394aa.jpg",
"https://telegra.ph/file/45eb08dd858d7e64f13c7.jpg",
"https://telegra.ph/file/911d76265b0951b9645e4.jpg",
"https://telegra.ph/file/f053ec6617e51007f38e2.jpg",
"https://telegra.ph/file/567ac614ad9ef0d756833.jpg",
"https://telegra.ph/file/c62381eccbdada2d42e0d.jpg",
"https://telegra.ph/file/040959b029ec920fd700e.jpg",
"https://telegra.ph/file/1d3e0e65420f7fc9bf6c3.jpg",
"https://telegra.ph/file/28d49e2214838939206c9.jpg",
"https://telegra.ph/file/4828bf8eb1e55ba7d76b0.jpg",
"https://telegra.ph/file/71176caf11f43d2a18a3c.jpg",
"https://telegra.ph/file/71176caf11f43d2a18a3c.jpg",
"https://telegra.ph/file/619839a00ed4ad14e97f7.jpg",
"https://telegra.ph/file/bf93a99e442a6c75e2640.jpg",
"https://telegra.ph/file/68dcd0c6f1351029341d7.jpg",
"https://telegra.ph/file/58d4bc68996c61e83a561.jpg",
"https://telegra.ph/file/e1bc8dd452a4f95c5bbc4.jpg",
"https://telegra.ph/file/be7664dcceb82112fb40b.jpg",
"https://telegra.ph/file/af832ded6d2a7ba795222.jpg",
"https://telegra.ph/file/2d7603ce18103a7b9b19b.jpg",
"https://telegra.ph/file/fa88b03dc55eb15e4a13e.jpg",
"https://telegra.ph/file/868d630ddf9fb5da8ddc6.jpg",
"https://telegra.ph/file/5bb2de0012f7bc78abdb5.jpg",
"https://telegra.ph/file/8d159e501d9cafc1314a8.jpg",
"https://telegra.ph/file/55edc3edb72f9d16fc429.jpg",
"https://telegra.ph/file/14b68ac33644ec695f08f.jpg",
"https://telegra.ph/file/a3b3dd1caf1bb24658405.jpg",
"https://telegra.ph/file/fdf34fb462a628a967b1b.jpg",
"https://telegra.ph/file/10c84a6fc44d32f6a0c70.jpg",
"https://telegra.ph/file/7d6a0effadf462bddf2f3.jpg",
"https://telegra.ph/file/6ef44068edd0436644ced.jpg",
"https://telegra.ph/file/e5b698001fd1e4a4a8be9.jpg",
"https://telegra.ph/file/a94bdc25a44db1c9b6162.jpg",
"https://telegra.ph/file/c95214281273ed2b80318.jpg",
"https://telegra.ph/file/e11b23c969108bac6a693.jpg",
"https://telegra.ph/file/392990303478131552f27.jpg",
"https://telegra.ph/file/15b52e85286fad6f69d59.jpg",
"https://telegra.ph/file/e2f967328ccd9d56e4e55.jpg",
"https://telegra.ph/file/b369e635ae772e43732df.jpg",
"https://telegra.ph/file/cbd60b36577023e8a7204.jpg",
"https://telegra.ph/file/5a825a38b8421b107186e.jpg",
"https://telegra.ph/file/bfc09bd6033dc2c5a662b.jpg",
"https://telegra.ph/file/692348069463ee6c6fa42.jpg",
"https://telegra.ph/file/e0aa9c395c193c49a2d56.jpg",
"https://telegra.ph/file/dc078659d2e0345d9fd49.jpg",
"https://telegra.ph/file/daa33bf67431c0c8b699c.jpg",
"https://telegra.ph/file/b6ff504d2f0b4f365ddb7.jpg",
"https://telegra.ph/file/2ba9c22cf31debac2e56d.jpg",
"https://telegra.ph/file/ec01fc9eb33b60a651a98.jpg",
"https://telegra.ph/file/85c14b1f93880f52e6970.jpg",
"https://telegra.ph/file/33a5192477b8ca1ae9836.jpg",
"https://telegra.ph/file/1d685ae9992113f9af18c.jpg",
"https://telegra.ph/file/95f7355b7f0694f13fdae.jpg"
                         ]

@register(pattern="^/logo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:

  if not quew:
     await event.reply('ᴩʟᴇᴀꜱᴇ ɢɪᴍᴍᴇ ᴀ ᴛᴇxᴛ ᴛᴏ ᴍᴀᴋᴇ yᴏᴜʀ ʟᴏɢᴏ ^_^.')
     return
 pesan = await event.reply('yᴏᴜʀ ʟᴏɢᴏ ɪꜱ ɪɴ ᴩʀᴏᴄᴇꜱꜱ...📩ᴩʟᴇᴀꜱᴇ ᴡᴀɪᴛ...!')
 try:
    text = event.pattern_match.group(1)
    randc = random.choice(LOGO_LINKS)
    img = Image.open(io.BytesIO(requests.get(randc).content))
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "black"
    shadowcolor = "blue"
    fnt = glob.glob("./EmikoRobot/utils/Logo/*")
    randf = random.choice(fnt)
    font = ImageFont.truetype(randf, 120)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y = ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="white", stroke_width=1, stroke_fill="black")
    fname = "Teddy.png"
    img.save(fname, "png")
    await telethn.send_file(event.chat_id, file=fname, caption = f"Made by @{SUPPORT_CHAT}")         
    await pesan.delete()
    if os.path.exists(fname):
            os.remove(fname)
 except Exception as e:
    await event.reply(f'Error, Report @{SUPPORT_CHAT}, {e}')



__mod_name__ = "Lᴏɢᴏ"

__help__ = """ ✘ Hᴇʟᴘ ᴍᴇɴᴜ ғᴏʀ ʟᴏɢᴏᴍᴀᴋᴇʀ ✘
➻ /logo Tᴇᴅᴅʏ - Cʀᴇᴀᴛᴇ ᴀ ʟᴏɢᴏ ᴡɪᴛʜ ʀᴀɴᴅᴏɴ ᴠɪᴇᴡ
"""
