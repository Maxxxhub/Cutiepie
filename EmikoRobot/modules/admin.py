import html

from telegram import ParseMode, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest, Unauthorized
from telegram.ext import CallbackContext, CommandHandler, Filters, run_async
from telegram.utils.helpers import mention_html

from EmikoRobot import DRAGONS, dispatcher
from EmikoRobot.modules.disable import DisableAbleCommandHandler
from EmikoRobot.modules.helper_funcs.chat_status import (
    bot_admin,
    can_pin,
    can_promote,
    connection_status,
    user_admin,
    ADMIN_CACHE,
)

from EmikoRobot.modules.helper_funcs.admin_rights import user_can_changeinfo, user_can_promote
from EmikoRobot.modules.helper_funcs.extraction import (
    extract_user,
    extract_user_and_text,
)
from EmikoRobot import SUPPORT_CHAT
from EmikoRobot.modules.log_channel import loggable
from EmikoRobot.modules.helper_funcs.alternate import send_message


@bot_admin
@user_admin
def set_sticker(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        return msg.reply_text("Yᴏᴜ ᴡᴇʀᴇ ᴍɪssɪɴɢ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ᴄʜᴀᴛ ɪɴғᴏ.!")

    if msg.reply_to_message:
        if not msg.reply_to_message.sticker:
            return msg.reply_text(
                "Yᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʀᴇᴘʟʏ ᴛᴏ sᴏᴍᴇ sᴛɪᴄᴋᴇʀ ᴛᴏ sᴇᴛ ᴀs ᴄʜᴀᴛ sᴛɪᴄᴋᴇʀ sᴇᴛ.!"
            )
        stkr = msg.reply_to_message.sticker.set_name
        try:
            context.bot.set_chat_sticker_set(chat.id, stkr)
            msg.reply_text(f"Sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ ɴᴇᴡ ɢʀᴏᴜᴘ sᴛɪᴄᴋᴇʀs ɪɴ {chat.title}!")
        except BadRequest as excp:
            if excp.message == "Participants_too_few":
                return msg.reply_text(
                    "Sᴏʟʟʏ, Dᴜᴇ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ ʀᴇsᴛʀɪᴄᴛɪᴏɴs ᴄʜᴀᴛ ɴᴇᴇᴅs ᴀᴛʟᴇᴀsᴛ 100 ᴍᴇᴍʙᴇʀs ʙᴇғᴏʀᴇ ᴛʜᴇʏ ᴄᴀɴ ʜᴀᴠᴇ ɢʀᴏᴜᴘ sᴛɪᴄᴋᴇʀs!"
                )
            msg.reply_text(f"Eʀʀᴏʀ! {excp.message}.")
    else:
        msg.reply_text("Yᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʀᴇᴘʟʏ ᴛᴏ sᴏᴍᴇ sᴛɪᴄᴋᴇʀ ᴛᴏ sᴇᴛ ᴀs ᴄʜᴀᴛ sᴛɪᴄᴋᴇʀ sᴇᴛ!")
       
    
@bot_admin
@user_admin
def setchatpic(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        msg.reply_text("Yᴏᴜ ᴡᴇʀᴇ ᴍɪssɪɴɢ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ɪɴғᴏ.!")
        return

    if msg.reply_to_message:
        if msg.reply_to_message.photo:
            pic_id = msg.reply_to_message.photo[-1].file_id
        elif msg.reply_to_message.document:
            pic_id = msg.reply_to_message.document.file_id
        else:
            msg.reply_text("Yᴏᴜ ᴄᴀɴ ᴏɴʟʏ sᴇᴛ sᴏᴍᴇ ᴘʜᴏᴛᴏ ᴀs ᴀ ᴄʜᴀᴛ ᴘɪᴄ.!")
            return
        dlmsg = msg.reply_text("Wᴀɪᴛ ᴀ sᴇᴄ...")
        tpic = context.bot.get_file(pic_id)
        tpic.download("gpic.png")
        try:
            with open("gpic.png", "rb") as chatp:
                context.bot.set_chat_photo(int(chat.id), photo=chatp)
                msg.reply_text("Sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ ɴᴇᴡ ᴄʜᴀᴛ ᴘɪᴄ!")
        except BadRequest as excp:
            msg.reply_text(f"Eʀʀᴏʀ! {excp.message}")
        finally:
            dlmsg.delete()
            if os.path.isfile("gpic.png"):
                os.remove("gpic.png")
    else:
        msg.reply_text("Rᴇᴘʟʏ ᴛᴏ sᴏᴍᴇ ᴘʜᴏᴛᴏ ᴏʀ ғɪʟᴇ ᴛᴏ sᴇᴛ ɪᴛ ᴀs ɴᴇᴡ ᴄʜᴀᴛ ᴘɪᴄ.!")
        
@bot_admin
@user_admin
def rmchatpic(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        msg.reply_text("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛs ᴛᴏ ᴅᴇʟᴇᴛᴇ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ.")
        return
    try:
        context.bot.delete_chat_photo(int(chat.id))
        msg.reply_text("Sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ᴛʜɪs ᴄʜᴀᴛ's ᴘʀᴏғɪʟᴇ ᴘʜᴏᴛᴏ!")
    except BadRequest as excp:
        msg.reply_text(f"Eʀʀᴏʀ! {excp.message}.")
        return
    
@bot_admin
@user_admin
def set_desc(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        return msg.reply_text("Yᴏᴜ'ʀᴇ ᴍɪssɪɴɢ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ᴄʜᴀᴛ ɪɴғᴏ!")

    tesc = msg.text.split(None, 1)
    if len(tesc) >= 2:
        desc = tesc[1]
    else:
        return msg.reply_text("Sᴇᴛᴛɪɴɢ ᴇᴍᴘᴛʏ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ᴅᴏᴇsɴ'ᴛ ᴍᴇᴀɴ ᴀɴʏᴛʜɪɴɢ!")
    try:
        if len(desc) > 255:
            return msg.reply_text("Dᴇsᴄʀɪᴘᴛɪᴏɴ ᴍᴜsᴛ ɴᴇᴇᴅs ᴛᴏ ʙᴇ ᴜɴᴅᴇʀ 255 ᴄʜᴀʀᴀᴄᴛᴇʀs!")
        context.bot.set_chat_description(chat.id, desc)
        msg.reply_text(f"Sᴜᴄᴄᴇssғᴜʟʟʏ ᴜᴘᴅᴀᴛᴇᴅ ᴄʜᴀᴛ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ɪɴ {chat.title}!")
    except BadRequest as excp:
        msg.reply_text(f"Eʀʀᴏʀ! {excp.message}.")        
        
@bot_admin
@user_admin
def setchat_title(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    args = context.args

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        msg.reply_text("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʜᴇ ᴄʜᴀᴛ ɪɴғᴏ!")
        return

    title = " ".join(args)
    if not title:
        msg.reply_text("Gɪᴍᴍᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ sᴇᴛ ᴀ ɴᴇᴡ ᴛɪᴛʟᴇ ғᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ!")
        return

    try:
        context.bot.set_chat_title(int(chat.id), str(title))
        msg.reply_text(
            f"Sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ <b>{title}</b> ᴀs ᴀ ɴᴇᴡ ᴄʜᴀᴛ ᴛɪᴛʟᴇ.!",
            parse_mode=ParseMode.HTML,
        )
    except BadRequest as excp:
        msg.reply_text(f"Eʀʀᴏʀ! {excp.message}.")
        return
        
        
@connection_status
@bot_admin
@can_promote
@user_admin
@loggable
def promote(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    promoter = chat.get_member(user.id)

    if (
        not (promoter.can_promote_members or promoter.status == "creator")
        and user.id not in DRAGONS
    ):
        message.reply_text("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ɴᴇᴄᴇꜱꜱᴀʀy ʀɪɢʜᴛꜱ ᴛᴏ ᴅᴏ ᴛʜᴀᴛ!")
        return

    user_id = extract_user(message, args)

    if not user_id:
        message.reply_text(
            "Yᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ᴛʜᴇ ID ꜱᴩᴇᴄɪꜰɪᴇᴅ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛ..",
        )
        return

    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if user_member.status in ('administrator', 'creator'):
        message.reply_text("Hᴏᴡ ᴀᴍ ɪ ᴍᴇᴀɴᴛ ᴛo ᴩʀᴏᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ ᴛʜᴀᴛ'ꜱ ᴀʟʀᴇᴀᴅy ᴀɴ ᴀᴅᴍɪɴ?")
        return

    if user_id == bot.id:
        message.reply_text("I ᴄᴀɴ'ᴛ ᴩʀᴏᴍᴏᴛᴇ ᴍyꜱᴇʟꜰ! ɢᴇᴛ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ɪᴛ ꜰᴏʀ ᴍᴇ.")
        return

    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = chat.get_member(bot.id)

    try:
        bot.promoteChatMember(
            chat.id,
            user_id,
            can_change_info=bot_member.can_change_info,
            can_post_messages=bot_member.can_post_messages,
            can_edit_messages=bot_member.can_edit_messages,
            can_delete_messages=bot_member.can_delete_messages,
            can_invite_users=bot_member.can_invite_users,
            can_manage_voice_chats=bot_member.can_manage_voice_chats,
            can_restrict_members=bot_member.can_restrict_members,
            can_pin_messages=bot_member.can_pin_messages,
        )
    except BadRequest as err:
        if err.message == "User_not_mutual_contact":
            message.reply_text("I caɴ'ᴛ ᴩʀᴏᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ ᴡʜᴏ ɪꜱɴ'ᴛ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴩ.")
        else:
            message.reply_text("Aɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ ᴡʜɪʟᴇ ᴩʀᴏᴍᴏᴛɪɴɢ.")
        return

    bot.sendMessage(
        chat.id,
        f"🖤Pʀᴏᴍᴏᴛɪɴɢ ᴀ ᴜꜱᴇʀ ɪɴ <b>{chat.title}</b>\n\nUꜱᴇʀ: {mention_html(user_member.user.id, user_member.user.first_name)}\nAᴅᴍɪɴ: {mention_html(user.id, user.first_name)}",
        parse_mode=ParseMode.HTML,
    )

    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"🤡#PROMOTED🤡\n"
        f"<b>📍Aᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>⚜️Uꜱᴇʀ:</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
    )

    return log_message


@connection_status
@bot_admin
@can_promote
@user_admin
@loggable
def lowpromote(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    promoter = chat.get_member(user.id)

    if (
        not (promoter.can_promote_members or promoter.status == "creator")
        and user.id not in DRAGONS
    ):
        message.reply_text("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ɴᴇᴄᴇꜱꜱᴀʀy ʀɪɢʜᴛꜱ ᴛᴏ ᴅᴏ ᴛʜᴀᴛ!")
        return

    user_id = extract_user(message, args)

    if not user_id:
        message.reply_text(
            "Yᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ᴛʜᴇ ID ꜱᴩᴇᴄɪꜰɪᴇᴅ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛ..",
        )
        return

    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if user_member.status in ('administrator', 'creator'):
        message.reply_text("Hᴏᴡ ᴀᴍ ɪ ᴍᴇᴀɴᴛ ᴛᴏ ᴩʀᴏᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ ᴛʜᴀᴛ'ꜱ ᴀʟʀᴇᴀᴅy ᴀɴ ᴀᴅᴍɪɴ?")
        return

    if user_id == bot.id:
        message.reply_text("I ᴄᴀɴ'ᴛ ᴩʀᴏᴍᴏᴛᴇ ᴍyꜱᴇʟꜰ! ɢᴇᴛ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ɪᴛ ꜰᴏʀ ᴍᴇ.")
        return

    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = chat.get_member(bot.id)

    try:
        bot.promoteChatMember(
            chat.id,
            user_id,
            can_delete_messages=bot_member.can_delete_messages,
            can_invite_users=bot_member.can_invite_users,
            can_pin_messages=bot_member.can_pin_messages,
        )
    except BadRequest as err:
        if err.message == "User_not_mutual_contact":
            message.reply_text("I caɴ'ᴛ ᴩʀᴏᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ ᴡʜᴏ ɪꜱɴ'ᴛ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴩ.")
        else:
            message.reply_text("Aɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ ᴡʜɪʟᴇ ᴩʀᴏᴍᴏᴛɪɴɢ.")
        return

    bot.sendMessage(
        chat.id,
        f"🖤Lᴏᴡᴩʀᴏᴍᴏᴛɪɴɢ ᴀ ᴜꜱᴇʀ ɪɴ <b>{chat.title}<b>\n\nUꜱᴇʀ: {mention_html(user_member.user.id, user_member.user.first_name)}\nAᴅᴍɪɴ: {mention_html(user.id, user.first_name)}",
        parse_mode=ParseMode.HTML,
    )

    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"🤡#LOWPROMOTED🤡\n"
        f"<b>📍Aᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>🖤Uꜱᴇʀ:</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
    )

    return log_message


@connection_status
@bot_admin
@can_promote
@user_admin
@loggable
def fullpromote(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    promoter = chat.get_member(user.id)

    if (
        not (promoter.can_promote_members or promoter.status == "creator")
        and user.id not in DRAGONS
    ):
        message.reply_text("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ɴᴇᴄᴇꜱꜱᴀʀy ʀɪɢʜᴛꜱ ᴛᴏ ᴅᴏ ᴛʜᴀᴛ!")
        return

    user_id = extract_user(message, args)

    if not user_id:
        message.reply_text(
            "Yᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ᴛʜᴇ ID ꜱᴩᴇᴄɪꜰɪᴇᴅ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛ..",
        )
        return

    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if user_member.status in ('administrator', 'creator'):
        message.reply_text("Hᴏᴡ ᴀᴍ ɪ ᴍᴇᴀɴᴛ ᴛᴏ ᴩʀᴏᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ ᴛʜᴀᴛ'ꜱ ᴀʟʀᴇᴀᴅy ᴀɴ ᴀᴅᴍɪɴ?")
        return

    if user_id == bot.id:
        message.reply_text("I ᴄᴀɴ'ᴛ ᴩʀᴏᴍᴏᴛᴇ ᴍyꜱᴇʟꜰ! ɢᴇᴛ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ɪᴛ ꜰᴏʀ ᴍᴇ.")
        return

    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = chat.get_member(bot.id)

    try:
        bot.promoteChatMember(
            chat.id,
            user_id,
            can_change_info=bot_member.can_change_info,
            can_post_messages=bot_member.can_post_messages,
            can_edit_messages=bot_member.can_edit_messages,
            can_delete_messages=bot_member.can_delete_messages,
            can_invite_users=bot_member.can_invite_users,
            can_promote_members=bot_member.can_promote_members,
            can_restrict_members=bot_member.can_restrict_members,
            can_pin_messages=bot_member.can_pin_messages,
            can_manage_voice_chats=bot_member.can_manage_voice_chats,
        )
    except BadRequest as err:
        if err.message == "User_not_mutual_contact":
            message.reply_text("I caɴ'ᴛ ᴩʀᴏᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ ᴡʜᴏ ɪꜱɴ'ᴛ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴩ.")
        else:
            message.reply_text("Aɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ ᴡʜɪʟᴇ ᴩʀᴏᴍᴏᴛɪɴɢ.")
        return

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            "Demote", callback_data="demote_({})".format(user_member.user.id))
    ]])

    bot.sendMessage(
        chat.id,
        f" 🖤Fᴜʟʟᴩʀᴏᴍᴏᴛɪɴɢ ᴀ ᴜꜱᴇʀ ɪɴ<b>{chat.title}</b>\n\n<b>Uꜱᴇʀ: {mention_html(user_member.user.id, user_member.user.first_name)}</b>\n<b>Pʀᴏᴍᴏᴛᴇʀ: {mention_html(user.id, user.first_name)}</b>",
        parse_mode=ParseMode.HTML,
    )

    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"🤡#FULLPROMOTED🤡\n"
        f"<b>📍Aᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>💥Uꜱᴇʀ:</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
    )

    return log_message


@connection_status
@bot_admin
@can_promote
@user_admin
@loggable
def demote(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(
            "Yᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ᴛʜᴇ ID ꜱᴩᴇᴄɪꜰɪᴇᴅ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛ..",
        )
        return

    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if user_member.status == "creator":
        message.reply_text("Tʜɪꜱ ᴩᴇʀꜱᴏɴ CREATED ᴛʜᴇ ᴄʜᴀᴛ, ʜᴏᴡ ᴡᴏᴜʟᴅ ɪ ᴅᴇᴍᴏᴛᴇ ᴛʜᴇᴍ?")
        return

    if not user_member.status == "administrator":
        message.reply_text("Cᴀɴ'ᴛ ᴅᴇᴍᴏᴛᴇ ᴡʜᴏ ᴡᴀsɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇᴅ!")
        return

    if user_id == bot.id:
        message.reply_text("Wʜʏ ɪ sʜᴏᴜʟᴅ ᴅᴇᴍᴏᴛᴇ ᴍʏsᴇʟғ ɴᴏᴏʙ, ʏᴏᴜ ᴋɪɴᴅᴀ ɴᴏᴏʙ ᴏʀ ᴡᴏᴛ!")
        return

    try:
        bot.promoteChatMember(
            chat.id,
            user_id,
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False,
            can_manage_voice_chats=False,
        )

        bot.sendMessage(
            chat.id,
            f"Sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇᴍᴏᴛᴇᴅ ᴀ ᴀᴅᴍɪɴ ɪɴ <b>{chat.title}</b>\n\n🥀Aᴅᴍɪɴ: <b>{mention_html(user_member.user.id, user_member.user.first_name)}</b>\n📍Dᴇᴍᴏᴛᴇʀ: {mention_html(user.id, user.first_name)}",
            parse_mode=ParseMode.HTML,
        )

        log_message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"🤡#DEMOTED🤡\n"
            f"<b>📍Admin:</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>🥀User:</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
        )

        return log_message
    except BadRequest:
        message.reply_text(
            "Cᴏᴜʟᴅ ɴᴏᴛ ᴅᴇᴍᴏᴛᴇ. I ᴍɪɢʜᴛ ɴᴏᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ , ᴏʀ ᴛʜᴇ ᴀᴅᴍɪɴ sᴛᴀᴛᴜs ᴡᴀs ᴀᴘᴘᴏɪɴᴛᴇᴅ ʙʏ ᴀɴᴏᴛʜᴇʀ"
            " ᴜsᴇʀ, Sᴏ ɪ ᴄᴀɴ'ᴛ ᴀᴄᴛ ᴜᴘᴏɴ ᴛʜᴇᴍ!",
        )
        return


@user_admin
def refresh_admin(update, _):
    try:
        ADMIN_CACHE.pop(update.effective_chat.id)
    except KeyError:
        pass

    update.effective_message.reply_text("Aᴅᴍɪɴ-ᴄᴀᴄʜᴇ ʀᴇғʀᴇsʜᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅!")


@connection_status
@bot_admin
@can_promote
@user_admin
def set_title(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args

    chat = update.effective_chat
    message = update.effective_message

    user_id, title = extract_user_and_text(message, args)
    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if not user_id:
        message.reply_text(
            "Yᴏᴜ ᴅᴏɴ'ᴛ sᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜsᴇʀ ᴏʀ ᴛʜᴇ ɪᴅ sᴘᴇᴄɪғɪᴇᴅ ɪs ɪɴᴄᴏʀʀᴇᴄᴛ...",
        )
        return

    if user_member.status == "creator":
        message.reply_text(
            "Tʜɪs ᴘᴇʀsᴏɴ CREATED ᴛʜᴇ ᴄʜᴀᴛ, Hᴏᴡ ᴄᴀɴ ɪ sᴇᴛ ᴄᴜsᴛᴏᴍ ᴛɪᴛʟᴇ ғᴏʀ ʜɪᴍ?",
        )
        return

    if user_member.status != "administrator":
        message.reply_text(
            "Cᴀɴ'ᴛ sᴇᴛ ᴛɪᴛʟᴇ ғᴏʀ ɴᴏɴ ᴀᴅᴍɪɴs!\nPʀᴏᴍᴏᴛᴇ ᴛʜᴇᴍ ғɪʀsᴛ, ᴛᴏ sᴇᴛ ᴄᴜsᴛᴏᴍ ᴛɪᴛʟᴇ!",
        )
        return

    if user_id == bot.id:
        message.reply_text(
            "I ᴄᴀɴ'ᴛ sᴇᴛ ᴍʏ ᴏᴡɴ ᴛɪᴛʟᴇ ᴍʏsᴇʟғ! Gᴇᴛ ᴛʜᴇ ᴏɴᴇ ᴡʜᴏ ᴍᴀᴅᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ɪᴛ ғᴏʀ ᴍᴇ.",
        )
        return

    if not title:
        message.reply_text("Sᴇᴛᴛɪɴɢ ʙʟᴀɴᴋ ᴛɪᴛʟᴇ ᴅᴏᴇsɴ'ᴛ ᴅᴏ ᴀɴʏᴛʜɪɴɢ!")
        return

    if len(title) > 16:
        message.reply_text(
            "Tʜᴇ ᴛɪᴛʟᴇ ʟᴇɴɢᴛʜ ɪs ʟᴏɴɢᴇʀ ᴛʜᴀɴ 16 ᴄʜᴀʀᴀᴄᴛᴇʀs...\nTʀᴜɴᴄᴀᴛɪɴɢ ɪᴛ ᴛᴏ 16 ᴄʜᴀʀᴀᴄᴛᴇʀs.!.",
        )

    try:
        bot.setChatAdministratorCustomTitle(chat.id, user_id, title)
    except BadRequest:
        message.reply_text(
            "Eɪᴛʜᴇʀ ᴛʜᴇʏ ᴀʀᴇɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇᴅ ʙʏ ᴍᴇ ᴏʀ ʏᴏᴜ sᴇᴛ ᴀ ᴛɪᴛʟᴇ ᴡʜɪᴄʜ ɪsɴ'ᴛ ᴘᴏssɪʙʟᴇ ᴛᴏ sᴇᴛ ."
        )
        return

    bot.sendMessage(
        chat.id,
        f" ✅ Sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ ᴛɪᴛʟᴇ ғᴏʀ <code>{user_member.user.first_name or user_id}</code> "
        f"ᴛᴏ <code>{html.escape(title[:16])}</code>!",
        parse_mode=ParseMode.HTML,
    )


@bot_admin
@can_pin
@user_admin
@loggable
def pin(update: Update, context: CallbackContext) -> str:
    bot, args = context.bot, context.args
    user = update.effective_user
    chat = update.effective_chat
    msg = update.effective_message
    msg_id = msg.reply_to_message.message_id if msg.reply_to_message else msg.message_id

    if msg.chat.username:
        # If chat has a username, use this format
        link_chat_id = msg.chat.username
        message_link = f"https://t.me/{link_chat_id}/{msg_id}"
    elif (str(msg.chat.id)).startswith("-100"):
        # If chat does not have a username, use this
        link_chat_id = (str(msg.chat.id)).replace("-100", "")
        message_link = f"https://t.me/c/{link_chat_id}/{msg_id}"

    is_group = chat.type not in ("private", "channel")
    prev_message = update.effective_message.reply_to_message

    if prev_message is None:
        msg.reply_text("Rᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴘɪɴ ɪᴛ!")
        return

    is_silent = True
    if len(args) >= 1:
        is_silent = (
            args[0].lower() != "notify"
            or args[0].lower() == "loud"
            or args[0].lower() == "violent"
        )

    if prev_message and is_group:
        try:
            bot.pinChatMessage(
                chat.id, prev_message.message_id, disable_notification=is_silent
            )
            msg.reply_text(
                f"I ʜᴀᴠᴇ ᴘɪɴɴᴇᴅ ᴀ ᴍᴇssᴀɢᴇ ☑️.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Gᴏ ᴛᴏ ᴍᴇꜱꜱᴀɢᴇ 🍫", url=f"{message_link}")
                        ]
                    ]
                ), 
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except BadRequest as excp:
            if excp.message != "Chat_not_modified":
                raise

        log_message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"🤡MESSAGE-PINNED-SUCCESSFULLY🤡\n"
            f"<b📍>Aᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}"
        )

        return log_message


@bot_admin
@can_pin
@user_admin
@loggable
def unpin(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message
    msg_id = msg.reply_to_message.message_id if msg.reply_to_message else msg.message_id
    unpinner = chat.get_member(user.id)

    if (
        not (unpinner.can_pin_messages or unpinner.status == "creator")
        and user.id not in DRAGONS
    ):
        message.reply_text("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ɴᴇᴠᴇssᴀʀʏ ʀɪɢʜᴛs ᴛᴏ ᴅᴏ ᴛʜᴀᴛ ⚒️!")
        return

    if msg.chat.username:
        # If chat has a username, use this format
        link_chat_id = msg.chat.username
        message_link = f"https://t.me/{link_chat_id}/{msg_id}"
    elif (str(msg.chat.id)).startswith("-100"):
        # If chat does not have a username, use this
        link_chat_id = (str(msg.chat.id)).replace("-100", "")
        message_link = f"https://t.me/c/{link_chat_id}/{msg_id}"

    is_group = chat.type not in ("private", "channel")
    prev_message = update.effective_message.reply_to_message

    if prev_message and is_group:
        try:
            context.bot.unpinChatMessage(
                chat.id, prev_message.message_id
            )
            msg.reply_text(
                f"📎Uɴᴘɪɴɴᴇᴅ <a href='{message_link}'>ᴛʜɪs ᴍᴇssᴀɢᴇ</a>.",
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except BadRequest as excp:
            if excp.message != "Chat_not_modified":
                raise

    if not prev_message and is_group:
        try:
            context.bot.unpinChatMessage(chat.id)
            msg.reply_text(
                "Uɴᴘɪɴɴᴇᴅ ᴛʜᴇ ʟᴀsᴛ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ."
            )
        except BadRequest as excp:
            if excp.message == "Mᴇssᴀɢᴇ ᴛᴏ ᴜɴᴘɪɴ ɴᴏᴛ ғᴏᴜɴᴅ 💀":
               msg.reply_text(
                   "I ᴄᴀɴ'ᴛ sᴇᴇ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ, Mᴀʏʙᴇ ᴀʟʀᴇᴀᴅʏ ᴜɴᴘɪɴɴᴇᴅ ᴏʀ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ ɢᴏᴛ ᴏʟᴅ ᴛᴏᴏ 🙂"
               )
            else:
                raise

    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"🤡MESSAGE-UNPINNED-SUCCESSFULLY🤡\n"
        f"<b>📍Aᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}"
    )

    return log_message


@bot_admin
def pinned(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    msg = update.effective_message
    msg_id = (
        update.effective_message.reply_to_message.message_id
        if update.effective_message.reply_to_message
        else update.effective_message.message_id
    )

    chat = bot.getChat(chat_id=msg.chat.id)
    if chat.pinned_message:
        pinned_id = chat.pinned_message.message_id
        if msg.chat.username:
            link_chat_id = msg.chat.username
            message_link = f"https://t.me/{link_chat_id}/{pinned_id}"
        elif (str(msg.chat.id)).startswith("-100"):
            link_chat_id = (str(msg.chat.id)).replace("-100", "")
            message_link = f"https://t.me/c/{link_chat_id}/{pinned_id}"

        msg.reply_text(
            f'🔽 Pɪɴɴᴇᴅ ᴏɴ {html.escape(chat.title)}.',
            reply_to_message_id=msg_id,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="👉 Gᴏ ᴛᴏ ᴍᴇꜱꜱᴀɢᴇ 🖇️", url=f"https://t.me/{link_chat_id}/{pinned_id}")]]
            ),
        )

    else:
        msg.reply_text(
            f"Tʜᴇʀᴇ ɪs ɴᴏ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ ɪɴ <b>{html.escape(chat.title)}!</b>",
            parse_mode=ParseMode.HTML,
        )


@bot_admin
@user_admin
@connection_status
def invite(update: Update, context: CallbackContext):
    bot = context.bot
    chat = update.effective_chat

    if chat.username:
        update.effective_message.reply_text(f"https://t.me/{chat.username}")
    elif chat.type in [chat.SUPERGROUP, chat.CHANNEL]:
        bot_member = chat.get_member(bot.id)
        if bot_member.can_invite_users:
            invitelink = bot.exportChatInviteLink(chat.id)
            update.effective_message.reply_text(invitelink)
        else:
            update.effective_message.reply_text(
                "I ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀᴄᴄᴇss ᴛᴏ ᴛʜᴇ ɪɴᴠɪᴛᴇ ʟɪɴᴋ, Tʀʏ ᴄʜᴀɴɢɪɴɢ ᴍʏ ᴘᴇʀᴍɪssɪᴏɴs!",
            )
    else:
        update.effective_message.reply_text(
            "I ᴄᴀɴ ᴏɴʟʏ ɢɪᴠᴇ ɪɴᴠɪᴛᴇ ʟɪɴᴋs ғᴏʀ sᴜᴘᴇʀɢʀᴏᴜᴘs ᴀɴᴅ ᴄʜᴀɴɴᴇʟs, Tʀʏ ᴄʜᴀɴɢɪɴɢ ʏᴏᴜʀ ɢʀᴏᴜᴘ ɪɴᴛᴏ sᴜᴘᴇʀɢʀᴏᴜᴘ ʙʏ ᴍᴀᴋɪɴɢ ɪᴛ ᴘᴜʙʟɪᴄ ☑!",
        )


@connection_status
def adminlist(update, context):
    chat = update.effective_chat  # type: Optional[Chat] -> unused variable
    user = update.effective_user  # type: Optional[User]
    args = context.args  # -> unused variable
    bot = context.bot

    if update.effective_message.chat.type == "private":
        send_message(update.effective_message, "Tʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘᴢ.")
        return

    chat = update.effective_chat
    chat_id = update.effective_chat.id
    chat_name = update.effective_message.chat.title  # -> unused variable

    try:
        msg = update.effective_message.reply_text(
            "Fᴇᴛᴄʜɪɴɢ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs..ᴘʟɪᴢ ᴡᴀɪᴛ!",
            parse_mode=ParseMode.HTML,
        )
    except BadRequest:
        msg = update.effective_message.reply_text(
            "Fᴇᴛᴄʜɪɴɢ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs..ᴘʟɪᴢ ᴡᴀɪᴛ!",
            quote=False,
            parse_mode=ParseMode.HTML,
        )

    administrators = bot.getChatAdministrators(chat_id)
    text = "Aᴅᴍɪɴs ɪɴ <b>{}</b>:".format(html.escape(update.effective_chat.title))

    for admin in administrators:
        user = admin.user
        status = admin.status
        custom_title = admin.custom_title

        if user.first_name == "":
            name = "☠ Deleted Account"
        else:
            name = "{}".format(
                mention_html(
                    user.id,
                    html.escape(user.first_name + " " + (user.last_name or "")),
                ),
            )

        if user.is_bot:
            administrators.remove(admin)
            continue

        # if user.username:
        #    name = escape_markdown("@" + user.username)
        if status == "creator":
            text += "\n 🚩 Cʀᴇᴀᴛᴏʀ:"
            text += "\n<code> • </code>{}\n".format(name)

            if custom_title:
                text += f"<code> ┗━ {html.escape(custom_title)}</code>\n"

    text += "\n⚜️ Aᴅᴍɪɴs:"

    custom_admin_list = {}
    normal_admin_list = []

    for admin in administrators:
        user = admin.user
        status = admin.status
        custom_title = admin.custom_title

        if user.first_name == "":
            name = "☠ Deleted Account"
        else:
            name = "{}".format(
                mention_html(
                    user.id,
                    html.escape(user.first_name + " " + (user.last_name or "")),
                ),
            )
        # if user.username:
        #    name = escape_markdown("@" + user.username)
        if status == "administrator":
            if custom_title:
                try:
                    custom_admin_list[custom_title].append(name)
                except KeyError:
                    custom_admin_list.update({custom_title: [name]})
            else:
                normal_admin_list.append(name)

    for admin in normal_admin_list:
        text += "\n<code> • </code>{}".format(admin)

    for admin_group in custom_admin_list.copy():
        if len(custom_admin_list[admin_group]) == 1:
            text += "\n<code> • </code>{} | <code>{}</code>".format(
                custom_admin_list[admin_group][0],
                html.escape(admin_group),
            )
            custom_admin_list.pop(admin_group)

    text += "\n"
    for admin_group, value in custom_admin_list.items():
        text += "\n🚨 <code>{}</code>".format(admin_group)
        for admin in value:
            text += "\n<code> • </code>{}".format(admin)
        text += "\n"

    try:
        msg.edit_text(text, parse_mode=ParseMode.HTML)
    except BadRequest:  # if original message is deleted
        return


@bot_admin
@can_promote
@user_admin
@loggable
def button(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    bot: Optional[Bot] = context.bot
    match = re.match(r"demote_\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        member = chat.get_member(user_id)
        bot_member = chat.get_member(bot.id)
        bot_permissions = promoteChatMember(
            chat.id,
            user_id,
            can_change_info=bot_member.can_change_info,
            can_post_messages=bot_member.can_post_messages,
            can_edit_messages=bot_member.can_edit_messages,
            can_delete_messages=bot_member.can_delete_messages,
            can_invite_users=bot_member.can_invite_users,
            can_promote_members=bot_member.can_promote_members,
            can_restrict_members=bot_member.can_restrict_members,
            can_pin_messages=bot_member.can_pin_messages,
            can_manage_voice_chats=bot_member.can_manage_voice_chats,
        )                
        demoted = bot.promoteChatMember(
                      chat.id,
                      user_id,
                      can_change_info=False,
                      can_post_messages=False,
                      can_edit_messages=False,
                      can_delete_messages=False,
                      can_invite_users=False,
                      can_restrict_members=False,
                      can_pin_messages=False,
                      can_promote_members=False,
                      can_manage_voice_chats=False,
        )
        if demoted:
        	update.effective_message.edit_text(
        	    f"Aᴅᴍɪɴ {mention_html(user.id, user.first_name)} sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇᴍᴏᴛᴇᴅ ☑️ {mention_html(member.user.id, member.user.first_name)}!",
        	    parse_mode=ParseMode.HTML,
        	)
        	query.answer("Demoted!")
        	return (
                    f"<b>{html.escape(chat.title)}:</b>\n" 
                    f"🤡#DEMOTE🤡\n" 
                    f"<b>📍Aᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
                    f"<b>🥀Usᴇʀ:</b> {mention_html(member.user.id, member.user.first_name)}"
                )
    else:
        update.effective_message.edit_text(
            "Tʜɪs ᴜsᴇʀ ᴡᴀs ɴᴏᴛ ᴘʀᴏᴍᴏᴛᴇᴅ ᴏʀ ʜᴀs ʟᴇғᴛ ᴛʜᴇ ᴄʜᴀᴛ/ɢʀᴏᴜᴘ!"
        )
        return ""


@connection_status
def bug_reporting(update: Update, _: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    bot = dispatcher.bot
    invitelink = bot.exportChatInviteLink(chat.id)
    puki = msg.text.split(None, 1)
    if len(puki) >= 2:
        bugnya = puki[1]
    else:
        msg.reply_text(
            "⚠️ <b>Yᴏᴜ ᴍᴜsᴛ sᴘᴇᴄɪғʏ ᴛʜᴇ ʙᴜɢ ᴄᴏɴᴛᴇɴᴛ ᴛᴏ ʀᴇᴘᴏʀᴛ ...</b>\n • Exᴀᴍᴘʟᴇ: <code>`/bug Mᴜsɪᴄ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ ᴏɴ ᴛᴇᴅᴅʏ`.</code>",
            parse_mode=ParseMode.HTML,
        )
        return

    try:
        if len(bugnya) > 100:
            return msg.reply_text("Bᴜɢ ᴍᴜsᴛ ɴᴇᴇᴅs ᴛᴏ ʙᴇ ᴜɴᴅᴇʀ 100 ᴄʜᴀʀᴄᴛᴇʀs..! Eʟsᴇ ᴊᴏɪɴ ʜᴇʀᴇ ᴛᴏ ʀᴇᴘᴏʀᴛ @Teddysupport ...!")
        bot.sendMessage(
            chat.id,
            f"✅ Yᴏᴜʀ ʙᴜɢ sᴜᴄᴄᴇssғᴜʟʟʏ sᴜʙᴍɪᴛᴛᴇᴅ ᴛᴏ <b>BOT ADMINS</b>. Tʜᴀɴᴋs ғᴏʀ ʀᴇᴘᴏʀᴛɪɴɢ ᴀ ʙᴜɢ ᴏɴ ᴛᴇᴅᴅʏ ʀᴏʙᴏᴛ...Sᴏᴏɴ, ᴛʜᴇ ʙᴏᴛ ᴀᴅᴍɪɴs ᴡɪʟʟ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ʀᴇᴘᴏʀᴛ/ʙᴜɢ...!\n Kᴇᴇᴘ sᴏᴍᴇ ᴘᴀᴛɪᴇɴᴄᴇ ɴᴅ sᴛᴀɴᴅ ᴡɪᴛʜ ᴛᴇᴅᴅʏ 🖤",
            parse_mode=ParseMode.HTML,
        )
        if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
            try:
                bot.sendMessage(
                    f"@{SUPPORT_CHAT}",
                    f"🎸<b>Nᴇᴡ ʙᴜɢ ʀᴇᴘᴏʀᴛᴇᴅ.!</b>\n\n<b>📄Cʜᴀᴛ :</b> <a href='{invitelink}'>{chat.title}</a>\n<b>📑Nᴀᴍᴇ:</b> <a href='tg://user?id={msg.from_user.id}'>{mention_html(msg.from_user.id, msg.from_user.first_name)}</a>\n<b>🔖Usᴇʀ ɪᴅ:</b> <code>{msg.from_user.id}</code>\n<b>🏷️Cʜᴀᴛ ɪᴅ:</b> <code>{chat.id}</code>\n\n🖇️Cᴏɴᴛᴇɴᴛ ɪɴ ʀᴇᴘᴏʀᴛ:\n{bugnya}",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Gᴏ ᴛᴏ ᴍᴇꜱꜱᴀɢᴇ", url=f"{msg.link}")]]
                    ),
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except Unauthorized:
                LOGGER.warning(
                    "Bot isnt able to send message to support_chat, go and check!"
                )
            except BadRequest as e:
                LOGGER.warning(e.message)
    except BadRequest:
        pass


__help__ =  """
*Usᴇʀ ᴄᴏᴍᴍᴀɴᴅs:*
➻ /admins*:* Lɪsᴛ ᴏғ ᴀᴅᴍɪɴs.
➻ /pinned*:* Tᴏ ɢᴇᴛ ᴄᴜʀʀᴇɴᴛ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ.
*Aᴅᴍɪɴs /-:*
➻ /pin*:* Sɪʟᴇɴᴛʟʏ ᴘɪɴ ᴛʜᴇ ᴍᴇssᴀɢᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ - ᴀᴅᴅ `'loud'` ᴏʀ `'notify'` ᴛᴏ ɢɪᴠᴇ ɴᴏᴛɪғs ᴛᴏ ᴜsᴇʀ$/ᴍᴇᴍʙᴇʀs.
➻ /unpin*:* Uɴᴘɪɴs ᴛʜᴇ ᴄᴜʀʀᴇɴᴛʟʏ ᴘɪɴɴᴇᴅ ᴍsɢ.
➻ /invitelink*:* Gᴇᴛs ɪɴᴠɪᴛᴇʟɪɴᴋ.
➻ /promote*:* Pʀᴏᴍᴏᴛᴇs ᴛʜᴇ ᴜsᴇʀ ʀᴇᴘʟɪᴇᴅ ᴛᴏ

➻ /fullpromote*:* Pʀᴏᴍᴏᴛᴇs ᴛʜᴇ ᴜsᴇʀ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴡɪᴛʜ ғᴜʟʟ ᴀᴅᴍɪɴ ʀɪɢʜᴛs.
➻ /demote*:* Dᴇᴍᴏᴛᴇs ᴛʜᴇ ᴜsᴇʀ ʀᴇᴘʟɪᴇᴅ ᴛᴏ.
➻ /title <title here>*:* Sᴇᴛs ᴀ ᴄᴜsᴛᴏᴍ ᴛɪᴛʟᴇ ғᴏʀ ᴀɴ ᴀᴅᴍɪɴ ᴡʜᴏ ɢᴏᴛ ᴘʀᴏᴍᴏᴛᴇᴅ ʙʏ ᴛᴇᴅᴅʏ ʙᴏᴛ.
➻ /admincache*:* Rᴇғʀᴇsʜ ᴛʜᴇ ᴀᴅᴍɪɴ ʟɪsᴛ.
"""

SET_DESC_HANDLER = CommandHandler("setdesc", set_desc, filters=Filters.chat_type.groups, run_async=True)
SET_STICKER_HANDLER = CommandHandler("setsticker", set_sticker, filters=Filters.chat_type.groups, run_async=True)
SETCHATPIC_HANDLER = CommandHandler("setgpic", setchatpic, filters=Filters.chat_type.groups, run_async=True)
RMCHATPIC_HANDLER = CommandHandler("delgpic", rmchatpic, filters=Filters.chat_type.groups, run_async=True)
SETCHAT_TITLE_HANDLER = CommandHandler("setgtitle", setchat_title, filters=Filters.chat_type.groups, run_async=True)

ADMINLIST_HANDLER = DisableAbleCommandHandler("admins", adminlist, run_async=True)
BUG_HANDLER = DisableAbleCommandHandler("bug", bug_reporting, run_async=True)

PIN_HANDLER = CommandHandler("pin", pin, filters=Filters.chat_type.groups, run_async=True)
UNPIN_HANDLER = CommandHandler("unpin", unpin, filters=Filters.chat_type.groups, run_async=True)
PINNED_HANDLER = CommandHandler("pinned", pinned, filters=Filters.chat_type.groups, run_async=True)

INVITE_HANDLER = DisableAbleCommandHandler("invitelink", invite, run_async=True)

PROMOTE_HANDLER = DisableAbleCommandHandler("promote", promote, run_async=True)
FULLPROMOTE_HANDLER = DisableAbleCommandHandler("fullpromote", fullpromote, run_async=True)
LOW_PROMOTE_HANDLER = DisableAbleCommandHandler("lowpromote", lowpromote, run_async=True)
DEMOTE_HANDLER = DisableAbleCommandHandler("demote", demote, run_async=True)

SET_TITLE_HANDLER = CommandHandler("title", set_title, run_async=True)
ADMIN_REFRESH_HANDLER = CommandHandler("admincache", refresh_admin, filters=Filters.chat_type.groups, run_async=True)

dispatcher.add_handler(SET_DESC_HANDLER)
dispatcher.add_handler(SET_STICKER_HANDLER)
dispatcher.add_handler(SETCHATPIC_HANDLER)
dispatcher.add_handler(RMCHATPIC_HANDLER)
dispatcher.add_handler(SETCHAT_TITLE_HANDLER)
dispatcher.add_handler(ADMINLIST_HANDLER)
dispatcher.add_handler(PIN_HANDLER)
dispatcher.add_handler(UNPIN_HANDLER)
dispatcher.add_handler(BUG_HANDLER)
dispatcher.add_handler(PINNED_HANDLER)
dispatcher.add_handler(INVITE_HANDLER)
dispatcher.add_handler(PROMOTE_HANDLER)
dispatcher.add_handler(FULLPROMOTE_HANDLER)
dispatcher.add_handler(LOW_PROMOTE_HANDLER)
dispatcher.add_handler(DEMOTE_HANDLER)
dispatcher.add_handler(SET_TITLE_HANDLER)
dispatcher.add_handler(ADMIN_REFRESH_HANDLER)

__mod_name__ = "Aᴅᴍɪɴꜱ"
__command_list__ = [
    "setdesc"
    "setsticker"
    "setgpic"
    "delgpic"
    "setgtitle"
    "adminlist",
    "admins", 
    "invitelink", 
    "promote", 
    "fullpromote",
    "lowpromote",
    "demote", 
    "admincache"
]
__handlers__ = [
    SET_DESC_HANDLER,
    SET_STICKER_HANDLER,
    SETCHATPIC_HANDLER,
    RMCHATPIC_HANDLER,
    SETCHAT_TITLE_HANDLER,
    ADMINLIST_HANDLER,
    PIN_HANDLER,
    UNPIN_HANDLER,
    PINNED_HANDLER,
    INVITE_HANDLER,
    PROMOTE_HANDLER,
    FULLPROMOTE_HANDLER,
    LOW_PROMOTE_HANDLER,
    DEMOTE_HANDLER,
    SET_TITLE_HANDLER,
    ADMIN_REFRESH_HANDLER,
]
