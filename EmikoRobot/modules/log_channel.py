from datetime import datetime
from functools import wraps
from telegram.ext import CallbackContext
from EmikoRobot.modules.helper_funcs.misc import is_module_loaded

FILENAME = __name__.rsplit(".", 1)[-1]

if is_module_loaded(FILENAME):
    from telegram import ParseMode, Update
    from telegram.error import BadRequest, Unauthorized
    from telegram.ext import CommandHandler, JobQueue, run_async
    from telegram.utils.helpers import escape_markdown

    from EmikoRobot import EVENT_LOGS, LOGGER, dispatcher
    from EmikoRobot.modules.helper_funcs.chat_status import user_admin
    from EmikoRobot.modules.sql import log_channel_sql as sql

    def loggable(func):
        @wraps(func)
        def log_action(
            update: Update,
            context: CallbackContext,
            job_queue: JobQueue = None,
            *args,
            **kwargs,
        ):
            if not job_queue:
                result = func(update, context, *args, **kwargs)
            else:
                result = func(update, context, job_queue, *args, **kwargs)

            chat = update.effective_chat
            message = update.effective_message

            if result:
                datetime_fmt = "%H:%M - %d-%m-%Y"
                result += f"\n<b>Eᴠᴇɴᴛ sᴛᴀᴍᴘ</b>: <code>{datetime.utcnow().strftime(datetime_fmt)}</code>"

                if message.chat.type == chat.SUPERGROUP and message.chat.username:
                    result += f'\n<b>Lɪɴᴋ:</b> <a href="https://t.me/{chat.username}/{message.message_id}">click here</a>'
                log_chat = sql.get_chat_log_channel(chat.id)
                if log_chat:
                    send_log(context, log_chat, chat.id, result)

            return result

        return log_action

    def gloggable(func):
        @wraps(func)
        def glog_action(update: Update, context: CallbackContext, *args, **kwargs):
            result = func(update, context, *args, **kwargs)
            chat = update.effective_chat
            message = update.effective_message

            if result:
                datetime_fmt = "%H:%M - %d-%m-%Y"
                result += "\n<b>Eᴠᴇɴᴛ sᴛᴀᴍᴘ</b>: <code>{}</code>".format(
                    datetime.utcnow().strftime(datetime_fmt)
                )

                if message.chat.type == chat.SUPERGROUP and message.chat.username:
                    result += f'\n<b>Lɪɴᴋ:</b> <a href="https://t.me/{chat.username}/{message.message_id}">click here</a>'
                log_chat = str(EVENT_LOGS)
                if log_chat:
                    send_log(context, log_chat, chat.id, result)

            return result

        return glog_action

    def send_log(
        context: CallbackContext, log_chat_id: str, orig_chat_id: str, result: str
    ):
        bot = context.bot
        try:
            bot.send_message(
                log_chat_id,
                result,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except BadRequest as excp:
            if excp.message == "Chat not found":
                bot.send_message(
                    orig_chat_id, "Tʜɪs ʟᴏɢ ᴄʜᴀɴɴᴇʟ ʜᴀs ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ - uɴsᴇᴛᴛɪɴɢ."
                )
                sql.stop_chat_logging(orig_chat_id)
            else:
                LOGGER.warning(excp.message)
                LOGGER.warning(result)
                LOGGER.exception("Could not parse")

                bot.send_message(
                    log_chat_id,
                    result
                    + "\n\nFᴏʀᴍᴀᴛᴛɪɴɢ ʜᴀs ʙᴇᴇɴ ᴅɪsᴀʙʟᴇᴅ ᴅᴜᴇ ᴛᴏ ᴀɴ ᴜɴᴇxᴘᴇᴄᴛᴇᴅ ᴇʀʀᴏʀ.",
                )

    @user_admin
    def logging(update: Update, context: CallbackContext):
        bot = context.bot
        message = update.effective_message
        chat = update.effective_chat

        log_channel = sql.get_chat_log_channel(chat.id)
        if log_channel:
            log_channel_info = bot.get_chat(log_channel)
            message.reply_text(
                f"Tʜɪs ɢᴛᴏᴜᴘ ʜᴀs ᴀʟʟ ɪᴛ's ʟᴏɢs sᴇɴᴛ ᴛᴏ:"
                f" {escape_markdown(log_channel_info.title)} (`{log_channel}`)",
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            message.reply_text("Nᴏ ʟᴏɢ ᴄʜᴀɴɴᴇʟ ʜᴀs ʙᴇᴇɴ sᴇᴛ ғᴏʀ ᴛʜɪs ɢʀᴏᴜᴘ!")

    @user_admin
    def setlog(update: Update, context: CallbackContext):
        bot = context.bot
        message = update.effective_message
        chat = update.effective_chat
        if chat.type == chat.CHANNEL:
            message.reply_text(
                "Nᴏᴡ, ғᴏʀᴡᴀʀᴅ ᴛʜᴇ /setlog ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴛɪᴇ ᴛʜɪs ᴄʜᴀɴɴᴇʟ ᴛᴏ!"
            )

        elif message.forward_from_chat:
            sql.set_chat_log_channel(chat.id, message.forward_from_chat.id)
            try:
                message.delete()
            except BadRequest as excp:
                if excp.message == "Message to delete not found":
                    pass
                else:
                    LOGGER.exception(
                        "Eʀʀᴏʀ ᴅᴇʟᴇᴛɪɴɢ ᴍsɢ ɪɴ ʟᴏɢ ᴄʜᴀɴɴᴇʟ. Sʜᴏᴜʟᴅ ᴡᴏʀᴋ ᴀɴʏᴡᴀʏ ᴛʜᴏᴜɢʜ."
                    )

            try:
                bot.send_message(
                    message.forward_from_chat.id,
                    f"Tʜɪs ᴄʜᴀɴɴᴇʟ ʜᴀs ʙᴇᴇɴ sᴇᴛ ᴀs ᴛʜᴇ ʟᴏɢ ᴄʜᴀɴɴᴇʟ ғᴏʀ {chat.title or chat.first_name}.",
                )
            except Unauthorized as excp:
                if excp.message == "Fᴏʀʙɪᴅᴅᴇɴ: Bᴏᴛ ɪs ɴᴏᴛ ᴀ ᴍᴇᴍʙᴇʀ ᴏғ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ᴄʜᴀᴛ":
                    bot.send_message(chat.id, "Sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ ʟᴏɢ ᴄʜᴀɴɴᴇʟ!")
                else:
                    LOGGER.exception("ERROR ɪɴ sᴇᴛᴛɪɴɢ ᴛʜᴇ ʟᴏɢ ᴄʜᴀɴɴᴇʟ.")

            bot.send_message(chat.id, "Sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ ʟᴏɢ ᴄʜᴀɴɴᴇʟ!")

        else:
            message.reply_text(
                "Sᴛᴇᴘs ᴛᴏ sᴇᴛ ᴀ ʟᴏɢ ᴄʜᴀɴɴᴇʟ ᴀʀᴇ:\n"
                " - Aᴅᴅ ʙᴏᴛ ᴛᴏ ᴛʜᴇ ᴅᴇsɪʀᴇᴅ ᴄʜᴀɴɴᴇʟ\n"
                " - Sᴇɴᴅ /setlog ᴛᴏ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ\n"
                " - Fᴏʀᴡᴀʀᴅ ᴛʜᴇ /setlog ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ\n"
            )

    @user_admin
    def unsetlog(update: Update, context: CallbackContext):
        bot = context.bot
        message = update.effective_message
        chat = update.effective_chat

        log_channel = sql.stop_chat_logging(chat.id)
        if log_channel:
            bot.send_message(
                log_channel, f"Cʜᴀɴɴᴇʟ ʜᴀs ʙᴇᴇɴ ᴜɴʟɪɴᴋᴇᴅ ғʀᴏᴍ {chat.title}"
            )
            message.reply_text("Lᴏɢ ᴄʜᴀɴɴᴇʟ ʜᴀs ʙᴇᴇɴ ᴜɴ-sᴇᴛ.")

        else:
            message.reply_text("Nᴏ ʟᴏɢ ᴄʜᴀɴɴᴇʟ ʜᴀs ʙᴇᴇɴ sᴇᴛ ʏᴇᴛ!")

    def __stats__():
        return f"× {sql.num_logchannels()} ʟᴏɢ ᴄʜᴀɴɴᴇʟs sᴇᴛ."

    def __migrate__(old_chat_id, new_chat_id):
        sql.migrate_chat(old_chat_id, new_chat_id)

    def __chat_settings__(chat_id, user_id):
        log_channel = sql.get_chat_log_channel(chat_id)
        if log_channel:
            log_channel_info = dispatcher.bot.get_chat(log_channel)
            return f"Tʜɪs ɢʀᴏᴜᴘ ʜᴀs ᴀʟʟ ɪᴛ's ʟᴏɢs sᴇᴍᴛ ᴛᴏ: {escape_markdown(log_channel_info.title)} (`{log_channel}`)"
        return "Nᴏ ʟᴏɢ ᴄʜᴀɴɴᴇʟ ɪs sᴇᴛ ғᴏʀ ᴛʜɪs ɢʀᴏᴜᴘ!"


    __help__ = """
──「 Lᴏɢ ᴄʜᴀɴɴᴇʟ 」──
➻ /logchannel*:* Gᴇᴛ ʟᴏɢ ᴄʜᴀɴɴᴇʟ ɪɴғᴏ.
➻ /setlog*:* Sᴇᴛ ᴛʜᴇ ʟᴏɢ ᴄʜᴀɴɴᴇʟ.
➻ /unsetlog*:* Uɴsᴇᴛ ᴛʜᴇ ʟᴏɢ ᴄʜᴀɴɴᴇʟ.
*SETTING THE LOG CHANNEL IS DONE BY*:
➩ Aᴅᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴛʜᴇ ᴅᴇsɪʀᴇᴅ ᴄʜᴀɴɴᴇʟ(ᴀs ᴀɴ ᴀᴅᴍɪɴ!)
➩ Sᴇɴᴅɪɴɢ /setlog ɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ.
➩ Fᴏʀᴡᴀʀᴅɪɴɢ ᴛʜᴇ /setlog ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ.
"""

    __mod_name__ = "Lᴏɢ ᴄʜᴀɴɴᴇʟ"

    LOG_HANDLER = CommandHandler("logchannel", logging, run_async=True)
    SET_LOG_HANDLER = CommandHandler("setlog", setlog, run_async=True)
    UNSET_LOG_HANDLER = CommandHandler("unsetlog", unsetlog, run_async=True)

    dispatcher.add_handler(LOG_HANDLER)
    dispatcher.add_handler(SET_LOG_HANDLER)
    dispatcher.add_handler(UNSET_LOG_HANDLER)

else:
    # run anyway if module not loaded
    def loggable(func):
        return func

    def gloggable(func):
        return func
