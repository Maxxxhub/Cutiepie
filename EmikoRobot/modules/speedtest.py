import speedtest
from EmikoRobot import DEV_USERS, dispatcher
from EmikoRobot.modules.disable import DisableAbleCommandHandler
from EmikoRobot.modules.helper_funcs.chat_status import dev_plus
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, run_async


def convert(speed):
    return round(int(speed) / 1048576, 2)


@dev_plus
@run_async
def speedtestxyz(update: Update, context: CallbackContext):
    buttons = [
        [
            InlineKeyboardButton("📷ɪᴍᴀɢᴇ", callback_data="speedtest_image"),
            InlineKeyboardButton("📄ᴛᴇxᴛ", callback_data="speedtest_text"),
        ]
    ]
    update.effective_message.reply_text(
        "sᴩᴇᴇᴅᴛᴇsᴛ ᴍᴏᴅᴇ", reply_markup=InlineKeyboardMarkup(buttons)
    )


@run_async
def speedtestxyz_callback(update: Update, context: CallbackContext):
    query = update.callback_query

    if query.from_user.id in DEV_USERS:
        msg = update.effective_message.edit_text("ʀᴜɴɴɪɴɢ ᴀ sᴩᴇᴇᴅᴛᴇsᴛ...")
        speed = speedtest.Speedtest()
        speed.get_best_server()
        speed.download()
        speed.upload()
        replymsg = "sᴩᴇᴇᴅᴛᴇsᴛ ʀᴇsᴜʟᴛ"

        if query.data == "speedtest_image":
            speedtest_image = speed.results.share()
            update.effective_message.reply_photo(
                photo=speedtest_image, caption=replymsg
            )
            msg.delete()

        elif query.data == "speedtest_text":
            result = speed.results.dict()
            replymsg += f"\n📥Dᴏᴡɴʟᴏᴀᴅ: `{convert(result['download'])}Mb/s`\n📤Uᴘʟᴏᴀᴅ: `{convert(result['upload'])}Mb/s`\n🏷️Pɪɴɢ ᴘᴏɴɢ: `{result['ping']}`"
            update.effective_message.edit_text(replymsg, parse_mode=ParseMode.MARKDOWN)
    else:
        query.answer("Yᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴊᴏɪɴ @Teddysupport ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")


SPEED_TEST_HANDLER = DisableAbleCommandHandler("speedtest", speedtestxyz)
SPEED_TEST_CALLBACKHANDLER = CallbackQueryHandler(
    speedtestxyz_callback, pattern="speedtest_.*"
)

dispatcher.add_handler(SPEED_TEST_HANDLER)
dispatcher.add_handler(SPEED_TEST_CALLBACKHANDLER)
