from flaskr.bot.owner.owner_constants import RECIEVE_ANNOUNCEMENT
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardRemove
from flaskr.bot.utils.is_owner import is_owner
from flaskr import db




def type_announcement(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_owner(update, context, session):
        return

    if 'announcement_message_id' in context.chat_data:
        del context.chat_data['announcement_message_id']

    update.message.reply_text(
        'ارسل رسالة نصية تحوي الاعلان. اقصر رسالة مسموحة 10 حروف.'
        , reply_markup=ReplyKeyboardRemove()
    )

    return RECIEVE_ANNOUNCEMENT