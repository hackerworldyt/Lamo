from telegram.ext.filters import Filters
from telegram import Update, message
from SaitamaRobot.modules.helper_funcs.decorator import vilcmd, vilmsg

from telegram.ext import CallbackContext
import html
from ..modules.sql.antichannel_sql import antichannel_status, disable_antichannel, enable_antichannel
from SaitamaRobot.modules.helper_funcs.chat_status import (
    bot_admin,
    can_restrict,
    connection_status,
    is_user_admin,
    is_user_ban_protected,
    is_user_in_chat,
    user_admin,
    user_can_ban,
    can_delete,
)



@bot_admin
@can_restrict
@user_admin
@vilcmd(command="antichannel", group=100)
def set_antichannel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    if len(args) > 0:
        s = args[0].lower()
        if s in ["yes", "on"]:
            enable_antichannel(chat.id)
            message.reply_html("Enabled antichannel in {}".format(html.escape(chat.title)))
        elif s in ["off", "no"]:
            disable_antichannel(chat.id)
            message.reply_html("Disabled antichannel in {}".format(html.escape(chat.title)))
        else:
            message.reply_text("Unrecognized arguments {}".format(s))
        return
    message.reply_html(
        "Antichannel setting is currently {} in {}".format(antichannel_status(chat.id), html.escape(chat.title)))


@vilmsg(Filters.chat_type.groups, group=110)
def eliminate_channel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    bot = context.bot
    if not antichannel_status(chat.id):
        return
    if message.sender_chat and message.sender_chat.type == "channel" and not message.is_automatic_forward:
        message.delete()
        sender_chat = message.sender_chat
        bot.ban_chat_sender_chat(sender_chat_id=sender_chat.id, chat_id=chat.id)

__mod_name__ = "Anti-Channel"
__help__ = """
Anti Channel helps you in stopping and banning channels

 • `/antichannel <on/off>`*:* enable anti channel
• *Admins only:*
"""
